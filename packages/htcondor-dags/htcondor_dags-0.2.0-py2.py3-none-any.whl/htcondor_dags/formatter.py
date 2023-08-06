# Copyright 2019 HTCondor Team, Computer Sciences Department,
# University of Wisconsin-Madison, WI.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Tuple

import abc

from . import exceptions

DEFAULT_SEPARATOR = ":"


class NodeNameFormatter(abc.ABC):
    def generate(self, layer_name: str, node_index: int) -> str:
        raise NotImplementedError

    def parse(self, node_name: str) -> Tuple[str, int]:
        raise NotImplementedError


class SimpleFormatter(NodeNameFormatter):
    def __init__(
        self, separator=DEFAULT_SEPARATOR, index_format="{:d}", offset: int = 0
    ):
        self.separator = separator
        self.index_format = index_format
        self.offset = offset

    def generate(self, layer_name: str, node_index: int) -> str:
        if self.separator in layer_name:
            raise exceptions.LayerNameContainsSeparator(
                f"The layer name {layer_name} cannot contain the node name separator character '{self.separator}'"
            )
        name = f"{layer_name}{self.separator}{self.index_format.format(node_index + self.offset)}"

        if self.parse(name) != (layer_name, node_index):
            raise exceptions.NoninvertibleFormat(
                f"{self.__class__.__name__} was not able to invert the formatted node name {name}. Perhaps the index_format is incompatible?"
            )

        return name

    def parse(self, node_name: str) -> Tuple[str, int]:
        layer, index = node_name.split(self.separator)
        return layer, int(index) - self.offset
