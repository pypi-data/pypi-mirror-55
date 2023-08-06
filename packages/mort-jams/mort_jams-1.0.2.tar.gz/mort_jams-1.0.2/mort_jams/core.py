import re
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Type, Union, cast

import srsly
from pydantic import BaseModel, Schema, fields


class UILabelValuePair(BaseModel):
    value: str
    label: str
    meta: Optional[str]


class UIFormattedString(BaseModel):
    """Useful when you want to specify a translation entry with format arguments"""

    key: str
    args: Dict[str, Union[int, float, str, bool]]


# Enumeration of types for valid select options
#
# Examples:
#   - [{value:"cool", label:"Cool Project"}]
#   - [10,4,3,12]
#   - [{value:12, label: "Administrator"}]
#   - ["cool","other","third"]
UISelectOptions = Union[UILabelValuePair, str, bool, int, float]


class UISchemaStep(BaseModel):
    label: str
    description: Optional[str]


class UISchemaConfig(BaseModel):
    translate: Optional[bool] = Schema(  # type: ignore
        True,
        description="whether or not the labels should be interpreted as locale keys",
    )
    title: Optional[str]
    disabled: Optional[bool]
    readonly: Optional[bool]
    narrow: Optional[bool]
    steps: Optional[List[UISchemaStep]]
    order: Optional[List[str]] = Schema(  # type: ignore
        None, description="list of property names to determine form field order"
    )


class UICondition(BaseModel):
    type: Optional[Union[List[str], str]]

    # Python's type system isn't quite advanced enough (I think?)
    # to deal with validating that the properties given to this condition
    # match properties of the larger schema object. So we allow all
    # fields and assert about that elsewhere.
    class Config:
        extra = "allow"


class UIProp(BaseModel):
    class Config:
        """Do not allow extra properties. This throws errors about field name typos"""

        extra = "forbid"

    title: Optional[str]
    description: Optional[Union[str, Dict[str, str]]]
    help: Optional[str]
    widget: Optional[str]
    field: Optional[str]
    data: Optional[str]
    placeholder: Optional[str]
    autoFocus: Optional[bool]
    text: Optional[str]
    classes: Optional[str]
    disabled: Optional[Union[bool, str]]
    readonly: Optional[bool]
    icon: Optional[str]
    items: Optional[List[UISelectOptions]]
    step: Optional[int]
    messages: Optional[Dict[str, Union[UIFormattedString, str]]]
    conditions: Optional[List[UICondition]]


UIHidden = UIProp(widget="hidden")


class UISchema(BaseModel):
    config: Optional[UISchemaConfig]
    properties: Optional[Dict[str, UIProp]]


class FormProp(Schema):
    """Specify a property mapping between a recipe argument and prodigy's UI"""

    def __init__(
        self, default: Any, *, ui: Optional[UIProp] = None, **kwargs: Any,
    ) -> None:
        self.ui = ui
        super(FormProp, self).__init__(default, **kwargs)


class FormSchema(BaseModel):
    data: Dict[str, Any]
    ui: UISchema


class FormModel(BaseModel):
    """Base JSON+UI pydantic model. It supports frontend UI schema attributes
    and overrides the schema() method to output an object with both the JSONSchema
    and the UI attributes that inform how it should be rendered in the frontend."""

    class Config:
        extra = "forbid"  # Throw errors about unknown fields
        ui: Optional[UISchemaConfig]

    @classmethod
    def form_schema(cls, by_alias: bool = True) -> Dict[str, Any]:
        """Return a dictionary with "data" and "ui" properties.

         - data contains the JSONSchema from the pydantic model
         - ui contains the associated UI schema for the same model"""
        return FormSchema(
            data=cls.schema(by_alias=by_alias), ui=model_ui_schema(cls)
        ).dict()


def model_ui_schema(model: Type[FormModel]) -> Dict[str, object]:
    """Take a single ``model`` and generate the uiSchema for its type."""
    config: object = {}
    if hasattr(model.Config, "ui") and isinstance(model.Config.ui, UISchemaConfig):
        config = model.Config.ui.dict(skip_defaults=True)

    properties: Dict[str, Dict[str, Any]] = {}
    definitions: Dict[str, Any] = {}
    for k, f in model.__fields__.items():
        field: fields.Field = f
        if isinstance(field.schema, FormProp):
            schema = cast(FormProp, field.schema)
            if schema.ui is not None:
                name = field.name
                properties[name] = {}
                ui_properties = schema.ui.dict(skip_defaults=True)
                for key in ui_properties.keys():
                    value = ui_properties[key]
                    key = key
                    properties[name][key] = value

    out_schema = dict(config=config, properties=properties)
    return out_schema


class PamTokenClaims(BaseModel):
    exp: int = Schema(..., title="The expiration date of the token in UTC milliseconds")
    aud: str = Schema(..., title="The audience that the token is intended for")
    iss: str = Schema(..., title="The issuer of the auth token.")
