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
    logic [15:0] mult1;
    logic        done1, done2, done3;
    logic        start_r; 

    // 检测 start 上升沿，生成单周期脉冲
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) start_r <= '0;
        else        start_r <= start;
    end

    wire start_pulse = start & ~start_r; 

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            a_q     <= '0;
            b_q     <= '0;
            mult1   <= '0;
            result  <= '0;
            done1   <= '0;
            done2   <= '0;
            done3   <= '0;
        end
        else begin
            a_q   <= A;
            b_q   <= B;
            mult1 <= a_q * b_q;
            result <= mult1;

            // 用 start_pulse 只在上升沿触发一次
            done1  <= start_pulse;
            done2  <= done1;
            done3  <= done2;
        end
    end

    assign done = done3;
endmodule : three_cycle
