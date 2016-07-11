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

import http = require("http");
import path = require("path");
import moment = require("moment");

const hostname = "thetv.jp";
const port = 80;
const agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36";
const paths = {
    "terrestrial": "/table/terrestrial/tokyo/",
    "bs": "/table/bs/101_181/tokyo/"
};

export class Controller {
    constructor() {}

    call(mode: string, date: moment.Moment): string {
        const opt = this.getRequestOption(mode, date);
        let body: string;
        const req = http.request(opt, (res) => {
            res.setEncoding("utf8");
            res.on("data", (chunk) => {
                body = chunk;
            });
            res.on("end", () => {
                console.log("done");
            });
        });
        req.on('error', (e) => {
            console.log(`error on requesting: ${e.message}`);
        });
        req.end();
        return body;
    }

    private getRequestOption(mode: string, date: moment.Moment): http.RequestOptions {
        const date_str = date.format('YYYYMMDD');
        return {
            hostname: hostname,
            path: path.join(paths[mode], date_str),
            method: "GET",
            headers: {
                "User-Agent": agent
            }
        };
    }
}