from dataclasses import asdict
from typing import Any, Dict, List, Mapping, Optional

from spanlib.common.exceptions import ConfigInvalidError
from spanlib.infrastructure.span_config.base_mapper.base_mapper import BaseMapper
from spanlib.infrastructure.span_config.config_objects import TrainingConfig
from spanlib.infrastructure.span_config.config_objects.command import (
    Command,
    CommandType,
    ShellCommand,
    SparkSubmitCommand,
)
from spanlib.utils.common import as_dataclass

try:
    from span.utils.app_telemetry.prometheus import (
        metrics_scope,
        prometheus_deprecated_code_called,
    )

    run_in_server = True
except ImportError:
    run_in_server = False


class V1TrainConfigMapper(BaseMapper):
    @staticmethod
    def create_config_object(config_dict) -> TrainingConfig:
        mapper = V1TrainConfigMapper(config_dict)
        return as_dataclass(mapper, TrainingConfig, install=mapper.install_commands.content)

    @property
    def image(self) -> str:
        # reraise didn't work with property, let's check directly
        img = self.config_dict.get("image", None)
        if not img:
            raise ConfigInvalidError
        return img

    @property
    def install_commands(self) -> ShellCommand:
        return ShellCommand(content=self.config_dict.get("install", []))

    @property
    def script_commands(self) -> List[Command]:
        script_stanza = self._script_stanza
        commands = []
        if script_stanza:
            # new format
            for command_dict in script_stanza:
                command: Command
                for command_type, command_value in command_dict.items():
                    if command_type == CommandType.SHELL:
                        command = ShellCommand(content=command_value)
                    elif command_type == CommandType.SPARK_SUBMIT:
                        command = SparkSubmitCommand(
                            script=command_value.get("script"),
                            conf=command_value.get("conf", {}),
                            settings=command_value.get("settings", {}),
                        )
                    else:
                        raise ConfigInvalidError("Unrecognized command")
                    commands.append(command)
            return commands
        else:
            if run_in_server:
                scope_labels = metrics_scope.get_current().get()
                prometheus_deprecated_code_called.labels(
                    **asdict(scope_labels), target_name="old_train_config"
                ).inc()

            # old format
            spark_stanza = self._spark_stanza
            if spark_stanza:
                return [
                    SparkSubmitCommand(
                        script=self.config_dict["script"][0],
                        conf=spark_stanza.get("conf", {}),
                        settings=spark_stanza.get("settings", {}),
                    )
                ]
            return [ShellCommand(content=self.config_dict["script"])]

    @property
    def _script_stanza(self) -> List[Dict[str, Any]]:
        script = self.config_dict["script"]
        if len(script) == 0 or isinstance(script[0], str):
            return []
        return script

    @property
    def _spark_stanza(self) -> Optional[Dict[str, Any]]:
        return self.config_dict.get("spark", None)

    @property
    def parameters(self) -> Mapping[str, str]:
        return self.config_dict.get("parameters", {})

    @property
    def secret_names(self) -> List[str]:
        return self.config_dict.get("secrets", [])
