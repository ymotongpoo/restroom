//    Copyright 2016 Yoshi Yamaguchi
// 
//    Licensed under the Apache License, Version 2.0 (the "License");
//    you may not use this file except in compliance with the License.
//    You may obtain a copy of the License at
// 
//        http://www.apache.org/licenses/LICENSE-2.0
// 
//    Unless required by applicable law or agreed to in writing, software
//    distributed under the License is distributed on an "AS IS" BASIS,
//    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//    See the License for the specific language governing permissions and
//    limitations under the License.
"use strict";

import moment = require("moment");
import http = require("http");
import { Controller } from "./controller";

class Main {
    private now: moment.Moment;
    private controller: Controller;

    constructor() {
        this.now = moment().locale('jp');
        this.controller = new Controller();
    }

    main() {
        const body = this.controller.call("terrestrial", this.now);
        console.log(body);
    }
}

const main = new Main();
main.main();

