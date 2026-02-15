module three_cycle (
    input  logic        clk,
    input  logic        rst_n,
    input  logic        start,
    input  logic [7:0]  A,
    input  logic [7:0]  B,
    output logic        done,
    output logic [15:0] result
);
    logic [7:0]  a_q, b_q;
    logic [15:0] mult1, mult2;
    logic        done1, done2, done3, done_q;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            a_q     <= '0;
            b_q     <= '0;
            mult1   <= '0;
            mult2   <= '0;
            result  <= '0;
            done1   <= '0;
            done2   <= '0;
            done3   <= '0;
            done_q  <= '0;
        end
        else begin
            a_q   <= A;
            b_q   <= B;
            mult1 <= a_q * b_q;
            mult2 <= mult1;
            result <= mult2;

            done1  <= start && !done_q;
            done2  <= done1  && !done_q;
            done3  <= done2  && !done_q;
            done_q <= done3  && !done_q;
        end
    end

    assign done = done_q;
endmodule : three_cycle

