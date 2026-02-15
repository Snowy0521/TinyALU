module single_cycle (
    input  logic        clk,
    input  logic        rst_n,
    input  logic        start,
    input  logic [2:0]  op,
    input  logic [7:0]  A,
    input  logic [7:0]  B,
    output logic        done,
    output logic [15:0] result
);
    logic done_int;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            result   <= '0;
            done_int <= '0;
        end
        else begin
            done_int <= '0;  // default

            if (start && (op != 3'b000)) begin
                case (op[1:0])
                    2'b01:   result <= {8'b0, A} + {8'b0, B};   // 显式 zero-extend，消除 WIDTHEXPAND
                    2'b10:   result <= {8'b0, A} & {8'b0, B};
                    2'b11:   result <= {8'b0, A} ^ {8'b0, B};
                    default: result <= '0;
                endcase
                done_int <= 1'b1;
            end
        end
    end

    assign done = done_int;
endmodule : single_cycle
