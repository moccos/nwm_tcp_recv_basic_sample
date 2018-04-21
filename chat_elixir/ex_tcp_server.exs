defmodule ExTcpTest.Server do
  require Logger

  def init() do
    port = 33337
    Logger.info "[#{inspect self()}] Server start at port #{port}"
    case :gen_tcp.listen(port, [:binary, active: false]) do
      {:ok, socket} ->
        pid = spawn_link(fn -> loop_accept(socket) end)
        Logger.info "[#{inspect pid}] Acceptor start."
        {:ok, nil}
      {:error, reason} -> {:error, reason}
    end
  end

  defp loop_accept(ls_socket) do
    {:ok, socket} = :gen_tcp.accept(ls_socket)
    {:ok, {addr, port}} = :inet.sockname(socket)
    Logger.info "accepted: #{inspect addr}:#{inspect port}"
    pid = spawn(fn -> ExTcpTest.Receiver.start(socket) end)
    :gen_tcp.controlling_process(socket, pid)

    loop_accept(ls_socket)
  end
end

defmodule ExTcpTest.Receiver do
  require Logger

  def start(socket) do
    Logger.info "[#{inspect self()}] Receiver start. (peer #{inspect :inet.peername(socket)})]"
    loop(socket)
  end

  defp loop(socket, buf \\ <<>>) do
    :inet.setopts(socket, [{:active, :once}])
    receive do
      {:tcp, _socket, data} ->
        entire_data = buf <> data # <>はバイナリ結合演算子
        case process_received_data(entire_data) do
          {:ok, fragment} ->
            loop(socket, fragment)
          x -> x
        end
      {:tcp_closed, _socket} ->
        Logger.info "closed"
        {:ok, []}
    end
  end

  defp process_received_data(data) do
    case byte_size data do
      0 -> {:ok, <<>>}
      _ ->
        << type :: unsigned-integer-size(8), rest::binary >> = data
        try do
          case type do
            1 -> 
              << id::unsigned-integer-size(16), rest::binary>> = rest
              Logger.info "JOIN: id #{id} rest #{byte_size rest}"
              process_received_data(rest)
            2 ->
              << len::unsigned-integer-size(16), rest::binary>> = rest
              chat_len = 8 * len
              << chat::bitstring-size(chat_len), rest::binary>> = rest
              Logger.info "CHAT: #{chat} rest #{byte_size rest}"
              process_received_data(rest)
            3 ->
              Logger.info "LEAVE"
              {:close, "Leave"}
            x ->
              reason = "Unknown type #{x}"
              Logger.warn reason
              {:error, reason}
          end
        rescue
          _e in MatchError -> {:ok, data}  # 長さ不足はここに来る
          e -> {:error, e}
        end
    end
  end
end

ExTcpTest.Server.init()
IO.puts "Press return to exit."
IO.gets("")
