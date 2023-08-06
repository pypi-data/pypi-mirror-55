import re
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Type, Union, cast

import srsly
from pydantic import BaseModel, Schema, fields


class UIValuePair(BaseModel):
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
UISelectOptions = Union[UIValuePair, str, bool, int, float]


class StrictModel(BaseModel):
    class Config:
        extra = "forbid"


class UISchemaStep(StrictModel):
    """Text data to display for a single step in a form with multiple steps"""

    label: str
    description: Optional[str]


class UISchemaConfig(StrictModel):
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
    """Determine if a field should be shown based some combination of other
    fields in the Schema."""

    type: Optional[Union[List[str], str]]

    # Python's type system isn't quite advanced enough (I think?)
    # to deal with validating that the properties given to this condition
    # match properties of the larger schema object. So we allow all
    # fields and assert about that elsewhere.
    class Config:
        extra = "allow"


class UIProp(StrictModel):
    """Define UI attributes for the current FormProp"""

    title: Optional[str]
    description: Optional[Union[str, Dict[str, str]]]
    help: Optional[Union[str, UIFormattedString, Dict[str, str]]]
    widget: Optional[str]
    field: Optional[str]
    data: Optional[str]
    placeholder: Optional[str]
    autoFocus: Optional[bool]
    minimumRows: Optional[int]
    text: Optional[str]
    classes: Optional[str]
    disabled: Optional[Union[bool, str]]
    readonly: Optional[bool]
    icon: Optional[str]
    step: Optional[int]
    messages: Optional[Dict[str, Union[UIFormattedString, str]]]
    conditions: Optional[List[UICondition]]
    options: Optional[UISelectOptions]


UIHidden = UIProp(widget="hidden")


class UISchema(BaseModel):
    """UISchema object that is associated with a JSONSchema. Contains form
    configuration information, and a dictionary of properties."""

    config: UISchemaConfig
    properties: Dict[str, UIProp] = Schema({}, title="UISchemaProps")


class FormProp(Schema):
    """The base property constructor for a Schema form"""

    def __init__(
        self, default: Any, *, ui: Optional[UIProp] = None, **kwargs: Any,
    ) -> None:
        self.ui = ui
        super(FormProp, self).__init__(default, **kwargs)


class FormSchema(BaseModel):
    """Exported JSON+UI schema dictionary. JSONSchema is in `data` and ui is in `ui`"""

    data: Dict[str, Any]
    ui: UISchema


class FormModel(BaseModel):
    """Base JSON+UI pydantic model. Supports frontend UI schema attributes
    and a form_schema() method to output an object with both the JSONSchema
    and the UI attributes."""

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
        ).dict(skip_defaults=True)


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
                properties[name] = schema.ui.dict(skip_defaults=True)

    out_schema = dict(config=config, properties=properties)
    return out_schema
