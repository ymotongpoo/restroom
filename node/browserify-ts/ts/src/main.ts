/// <referene path="../../node_modules/@types/moment/index.d.ts" />
import * as moment from 'moment';

function main() {
    const today = moment();
    console.log(today.format("YYYYMMDD"));
}

main();