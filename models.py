from enum import Enum
from pydantic import BaseModel
from pydantic.fields import ModelField
from typing import Dict, Any
from types_validator import CheckModel, ModelsList, Params, ModelParams


class DataTypes(Enum):
    common_str = str
    common_int = int
    str_null = str
    int_null = int
    str_not_null = (str, ...)
    int_not_null = (int, ...)


DEFAULT_MODEL_LIST = {
    "fio": {
        "url": "http://asd.com/{}",
        "param_type": "body",
        "params": {
            "last_name": DataTypes.str_not_null.value,
            "first_name": DataTypes.str_not_null.value,
            "middle_name": DataTypes.str_null.value,
        }
    },
    "calc_sum": {
        "url": "http://asd.com/{}",
        "param_type": "body",
        "params": {
            "a": DataTypes.int_not_null.value,
            "b": DataTypes.int_not_null.value,
            "c": DataTypes.int_not_null.value,
        }
    }
}


class DynamicModel(BaseModel):

    @classmethod
    def add_fields(cls, **field_definitions: Any):
        new_fields: Dict[str, ModelField] = {}

        for f_name, f_def in field_definitions.items():
            if isinstance(f_def, tuple):
                try:
                    f_annotation, f_value = f_def
                except ValueError as e:
                    raise Exception(
                        'field definitions should either be a tuple of (<type>, <default>) or just a '
                        'default value, unfortunately this means tuples as '
                        'default values are not allowed'
                    ) from e
            else:
                f_annotation, f_value = f_def, None
            new_fields[f_name] = ModelField.infer(name=f_name, value=f_value, annotation=f_annotation,
                                                  class_validators=None, config=cls.__config__)

        cls.__fields__.update(new_fields)


class Models:
    models = {}

    @classmethod
    def load_models(cls):
        for model_name, model_fields in DEFAULT_MODEL_LIST.items():
            class ChildModel(DynamicModel):
                ...

            ChildModel.add_fields(**model_fields["params"])
            cls.models[model_name] = ChildModel

    @classmethod
    def load_model(cls, model_params: ModelParams):
        """
        :param model_params= {
          "name": "new_model_name",
          "params": [
            {"name": "param_name", "type": "str/int", "nullable": true/false},
            ...
          ]
        }
        :return: bool
        """
        class ChildModel(DynamicModel):
            ...

        model_name = model_params.name
        model_fields = {}
        print(model_params.params)
        for param in model_params.params:
            if param.type == DataTypes.common_str.value and param.nullable:
                model_fields[param.name] = DataTypes.str_null.value
            elif param.type == DataTypes.common_str.value and not param.nullable:
                model_fields[param.name] = DataTypes.str_not_null.value
            elif param.type == DataTypes.common_int.value and param.nullable:
                model_fields[param.name] = DataTypes.int_null.value
            elif param.type == DataTypes.common_int.value and not param.nullable:
                model_fields[param.name] = DataTypes.int_not_null.value

        ChildModel.add_fields(**model_fields)
        cls.models[model_name] = ChildModel

    @classmethod
    async def check_model(cls, model_name: str):
        return CheckModel(model_name=model_name, result=model_name in cls.models)

    @classmethod
    async def get_model_list(cls):
        return ModelsList(models=list(cls.models))
