from typing import Optional
import yaml
import jinja2
from jinja2 import Template
from enum import Enum, IntEnum
import copy
from pydantic import create_model, BaseModel as PydanticBaseModel, Field
# from ..pipeline import nodepred, nodepred_sample
from .factory import ModelFactory, PipelineFactory, DataFactory
from .base_model import DGLBaseModel

class DatasetEnum(str, Enum):
    RedditDataset = "RedditDataset"
    CoraGraphDataset = "CoraGraphDataset"

# class PipelineEnum(str, Enum):
#     nodepred = "nodepred"
#     nodepred_ns = 'nodepred_ns'
# PipelineEnum = PipelineFactory.get_pipeline_enum()

class DataConfig(DGLBaseModel):
    name: DatasetEnum

output_file_path = None

SamplerConfig = dict

class PipelineConfig(DGLBaseModel):    
    node_embed_size: Optional[int] = -1
    early_stop: Optional[dict]
    num_epochs: int = 200
    eval_period: int = 5
    optimizer: dict = {"name": "Adam", "lr": 0.005}
    loss: str = "CrossEntropyLoss"

class UserConfig(DGLBaseModel):
    version: Optional[str] = "0.0.1"
    pipeline_name: PipelineFactory.get_pipeline_enum()
    device: str = "cpu"
    data: DataFactory.get_pydantic_config() = Field(..., discriminator="name")
    model : ModelFactory.get_pydantic_model_config() = Field(..., discriminator="name")
    general_pipeline: PipelineConfig = PipelineConfig()

