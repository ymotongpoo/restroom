import std.json     : parseJSON;
import std.net.curl : get;
import std.array;


string show() {
    // Say show :-)
    return "show";
}


string latestStatus() {
    // Print latest bucho's tweet.
    immutable url = 
        "https://api.twitter.com/1/statuses/user_timeline.json?" ~
        "?screen_name=torufurukawa&include_rts=true";

    auto content = get(url);
    auto result = parseJSON(content);
    return result.array[0].object["text"].str;
}


string allStatus() {
    immutable url = 
        "https://api.twitter.com/1/statuses/user_timeline.json?" ~
        "?screen_name=torufurukawa&include_rts=true";
    auto content = get(url);
    auto result = parseJSON(content);
    string statuses = "";
    foreach(ref entry; result.array) {
        statuses ~= entry.object["text"].str ~ "\n";
    }
    return statuses;
}


