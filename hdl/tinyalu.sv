
module tinyalu (
    input   logic         clk,
    input   logic         rst_n,
    input   logic         start,
    input   logic [2:0]   op,
    input   logic [7:0]   A,
    input   logic [7:0]   B,
    output  logic         done,
    output  logic [15:0]  result
);

    // Internal signals
    logic           start_single;
    logic           start_multi;
    logic           done_aax;
    logic           done_mult;
    logic [15:0]    result_aax;
    logic [15:0]    result_mult;

    // Start signal mux
    always_comb begin
        case (op[2])
            1'b0: begin
                start_single = start;
                start_multi  = 1'b0;
            end
            1'b1: begin
                start_single = 1'b0;
                start_multi  = start;
            end
            default: begin
                start_single = 1'b0;
                start_multi  = 1'b0;
            end
        endcase
    end

    // Result mux
    always_comb begin
        case (op[2])
            1'b0: result = result_aax;
            1'b1: result = result_mult;
            default: result = 16'bx;
        endcase
    end

    // Done signal mux
    always_comb begin
        case (op[2])
            1'b0: done = done_aax;
            1'b1: done = done_mult;
            default: done = 1'bx;
        endcase
    end

    // Instantiate single-cycle module
    single_cycle u_aax (
        .clk(clk),
        .rst_n(rst_n),
        .start(start_single),
        .op(op),
        .A(A),
        .B(B),
        .done(done_aax),
        .result(result_aax)
    );

    // Instantiate three-cycle module
    three_cycle u_mult (
        .clk(clk),
        .rst_n(rst_n),
        .start(start_multi),
        .A(A),
        .B(B),
        .done(done_mult),
        .result(result_mult)
    );

endmodule : tinyalu


