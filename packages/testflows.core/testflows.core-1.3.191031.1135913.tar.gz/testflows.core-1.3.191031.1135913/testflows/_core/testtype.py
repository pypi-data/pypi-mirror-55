# Copyright 2019 Vitaliy Zakaznikov (TestFlows Test Framework http://testflows.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
class TestType(object):
    """Test type."""
    Module = 40
    Suite = 30
    Test = 20
    Run = 15
    Step = 10

class TestSubType(object):
    """Test behaviour subtype."""
    Feature = 60
    Scenario = 50
    Background = 40
    Given = 30
    When = 20
    Then = 10
    And = 8
    But = 7
    By = 6
    Finally = 5
    Empty = 0

