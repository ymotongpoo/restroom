(************************************************************)
(*                                                          *)
(*                  OCaml for memcached                     *)
(*                                                          *)
(* tested environment:                                      *)
(*   OCaml 3.11.2                                           *)
(*   memcache 1.4.5                                         *)
(*                                                          *)
(* OCaml binding for memcached.                             *)
(*                                                          *)
(************************************************************)


(*

TODO
  getmulti : hand multiple hostnames and keys, then get values from them
  there should be (key, host) hash table.

*)


module Memcached : sig

  open Unix

  val endline : string
    (** CRLF *)

  val connect : ?port:int -> string -> file_descr
    (** connect to memcached with hostname and port *)

  val version : file_descr -> string
    (** version command *)

  val set : file_descr -> string -> int -> int -> string -> string
    (** store data. [set sock key flags exptime msg] *)

  val add : file_descr -> string -> int-> int -> string -> string
    (** store data only if ther server DOESN'T already hold data for
        the key. [add sock key flags exptime msg]
    *)

  val replace : file_descr -> string -> int -> int -> string -> string
    (** store data only if the server DOES already hold data for the key.
        [replace sock key flags exptime msg]
    *)

  val append : file_descr -> string -> int -> int -> string -> string
    (** add data to an existing key after existing data.
        [append sock key flags exptime msg]
    *)

  val prepend : file_descr -> string -> int -> int -> string -> string
    (** add data to an existing key before existing data.
        [prepend sock key flags exptime msg]
    *)

  val cas : file_descr -> string -> int -> int -> int -> string -> string
    (** store data only if no one else has updated since I last fetched it.
        [cas sock key flags exptime msg casunique]. "cas unique" is aquired
        with "gets" command.
    *)

  val get : file_descr -> string -> string
    (** get item with key. [get sock key] *)

  val gets : file_descr -> string -> string
    (** get item with key. [gets sock key] *)

  val getmulti : file_descr list -> string list -> unit
    (** to be implemented *)

  val incr : file_descr -> string -> int -> int
    (** increment item. [incr key value] *)

  val decr : file_descr -> string -> int -> int
    (** decrement item. [decr key value] *)

  val delete : file_descr -> ?time:int -> string -> string
    (** delete item. [delete sock time key]. "time" is the amount of 
        time in seconds. default is 0.
    *)

  val stats : file_descr -> string list
    (** returns statistics. [stats sock]
    *)

  val flush_all : file_descr -> string
    (** flush all items *)

end = struct

  open Unix

  let endline = "\r\n";;


  let connect ?(port=11211) hostname = 
    let sock = socket PF_INET SOCK_STREAM 0 in
    let host = gethostbyname hostname in
    connect sock (ADDR_INET (host.h_addr_list.(0), port));
    sock
  ;;


  (** sock_send : file_descr -> string -> int *)
  let sock_send sock str =
    let len = String.length str in
    send sock str 0 len []
  ;;


  (** sock_recv : ?maxlen:int -> file_descr -> string *)
  let sock_recv ?(maxlen=1024) sock =
    let str = String.create maxlen in
    let recvlen = recv sock str 0 maxlen [] in
    String.sub str 0 recvlen
  ;;


  (** readline : split string with '\r\n' *)
  let readlines str =
    let elexp = Str.regexp "\r\n" in
    Str.split elexp str
  ;;

  
  let version sock =
    let _ = sock_send sock ("version" ^ endline) in
    sock_recv ~maxlen:20 sock
  ;;


  (** base store functions *)
  (**
     val store ; file_descr -> string -> int -> int -> int -> string -> string
  *)
  let store sock command key flags exptime msg = 
    let bytes = string_of_int (String.length msg) in
    let query = 
      [command; key; string_of_int flags; string_of_int exptime;
      bytes; endline] in
    let str = (String.concat " " query) ^ msg ^ endline in
    let _ = sock_send sock str in
    let recv = sock_recv sock in
    match recv with
    | "STORED\r\n" -> recv
    | "NOT_STORED\r\n" -> raise(Failure (command ^ ":not stored"))
    | "EXISTS\r\n" -> raise(Failure (command ^ ":not stored"))
    | "NOT_FOUND\r\n" -> raise(Failure (command ^ ":not stored"))
    | _ -> raise(Failure (command ^ ":not stored"))
  ;;


  let set sock key flags exptime msg =
    store sock "set" key flags exptime msg
  ;;


  let add sock key flags exptime msg = 
    store sock "add" key flags exptime msg
  ;;


  let replace sock key flags exptime msg =
    store sock "replace" key flags exptime msg
  ;;

  
  let append sock key flags exptime msg =
    store sock "append" key flags exptime msg
  ;;

  
  let prepend sock key flags exptime msg =
    store sock "prepend" key flags exptime msg
  ;;

  
  let cas sock key flags exptime casuniq msg =
    let bytes = string_of_int (String.length msg) in
    let query = 
      ["cas"; key; string_of_int flags; string_of_int exptime;
      bytes; string_of_int casuniq; endline] in
    let str = (String.concat " " query) ^ msg ^ endline in
    let _ = sock_send sock str in
    let recv = sock_recv sock in
    match recv with
    | "STORED\r\n" -> recv
    | "NOT_STORED\r\n" -> raise(Failure ("cas:not stored"))
    | "EXISTS\r\n" -> raise(Failure ("cas:not stored"))
    | "NOT_FOUND\r\n" -> raise(Failure ("cas:not stored"))
    | _ -> raise(Failure ("cas:not stored"))
  ;;
  

  let get sock key =
    let str = "get " ^ key ^ endline in
    let _ = sock_send sock str in
    let recv = sock_recv sock in
    match recv with
    | "END\r\n" -> ""
    | _ -> recv
  ;;


  let gets sock key =
    let str = "gets " ^ key ^ endline in
    let _ = sock_send sock str in
    let recv = sock_recv sock in
    match recv with
    | "END\r\n" -> ""
    | _ -> recv
  ;;


  let getmulti socks keys = ();;


  let incr sock key value =
    let query = ["incr"; key; string_of_int value] in
    let str = (String.concat " " query) ^ endline in
    let _ = sock_send sock str in
    let recvs = readlines (sock_recv sock) in
    match recvs with
    | ["ERROR"] -> raise(Failure "incr:error")
    | ["NOT_FOUND"] -> raise(Failure "incr:not found")
    | [x] -> int_of_string x
    | _ -> 0
  ;;


  let decr sock key value =
    let query = ["decr"; key; string_of_int value] in
    let str = (String.concat " " query) ^ endline in
    let _ = sock_send sock str in
    let recvs = readlines (sock_recv sock) in
    match recvs with
    | ["ERROR"] -> raise(Failure "decr:error")
    | ["NOT_FOUND"] -> raise(Failure "decr:not found")
    | [x] -> int_of_string x
    | _ -> 0
  ;;


  let delete sock ?(time=0) key =
    let query = ["delete"; key; string_of_int time] in
    let str = (String.concat " " query) ^ endline in
    let _ = sock_send sock str in
    let recv = sock_recv sock in
    match recv with
    | "DELETED\r\n" -> recv
    | "NOT_FOUND\r\n" -> raise(Failure "delete:not found")
    | _ -> raise(Failure "delete:unknown error")
  ;;


  let stats sock =
    let _ = sock_send sock "stats\r\n" in
    let recvs = List.rev (readlines (sock_recv sock)) in
    match recvs with
    | "END" :: _ -> List.rev recvs
    | _ -> raise(Failure "stats:receive error")
  ;;


  let flush_all sock =
    let _ = sock_send sock "flush_all\r\n" in
    sock_recv sock
  ;;

end;;

(**
   http://code.google.com/p/memcached/wiki/MemcacheBinaryProtocol
*)
module Bmemcached : sig

  open Unix

  val endline : string
    (** CRLF *)

  val connect : ?port:int -> string -> file_descr
    (** connect to memcached with hostname and port *)

  val version : file_descr -> string
    (** version command *)

  val set : file_descr -> string -> int -> int -> string -> string
    (** store data. [set sock key flags exptime msg] *)

  val add : file_descr -> string -> int-> int -> string -> string
    (** store data only if ther server DOESN'T already hold data for
        the key. [add sock key flags exptime msg]
    *)

end = struct

  open Unix

  let endline = "\r\n";;


  let connect ?(port=11211) hostname = 
    let sock = socket PF_INET SOCK_STREAM 0 in
    let host = gethostbyname hostname in
    connect sock (ADDR_INET (host.h_addr_list.(0), port));
    sock
  ;;


  (** sock_send : file_descr -> string -> int *)
  let sock_send sock str =
    let len = String.length str in
    send sock str 0 len []
  ;;


  (** sock_recv : ?maxlen:int -> file_descr -> string *)
  let sock_recv ?(maxlen=1024) sock =
    let str = String.create maxlen in
    let recvlen = recv sock str 0 maxlen [] in
    String.sub str 0 recvlen
  ;;


  (** readline : split string with '\r\n' *)
  let readlines str =
    let elexp = Str.regexp "\r\n" in
    Str.split elexp str
  ;;

  
  let version sock =
    let _ = sock_send sock ("version" ^ endline) in
    sock_recv ~maxlen:20 sock
  ;;


  (** request *)
  let request magic opc keylen extlen datat bodylen opaq cas =
    




  let bits filename = Bitstring.bitstring_of_file filename;;

end



let readlines str =
  let elexp = Str.regexp "\r\n" in
  Str.split elexp str
;;


let _ =
  let sock = Memcached.connect "localhost" in
  let _ = Memcached.set sock "foo" 0 0 "spam" in
  let _ = Memcached.set sock "bar" 0 0 "egg" in
  let _ = Memcached.set sock "num" 0 0 "1" in
  let recvd = Memcached.get sock "foo" in
  begin
    Printf.printf "received -> %s\n%!" (List.nth (readlines recvd) 1);
    Printf.printf "version -> %s\n%!" (Memcached.version sock);
    Printf.printf "incremented -> %d\n%!" (Memcached.incr sock "num" 3);
    Printf.printf "decremented -> %d\n%!" (Memcached.decr sock "num" 2);
    Printf.printf "stats %s%!\n" (String.concat "\n" (Memcached.stats sock));
    Memcached.flush_all;
  end
;;
