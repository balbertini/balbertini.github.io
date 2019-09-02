--------------------------------------------------------------------------------
--! @file registrador_tb.vhdl
--! @author balbertini@usp.br
--! @date 20190902
--! @brief TestBench para o registrador com FFD.
--------------------------------------------------------------------------------
library ieee;
use ieee.numeric_bit.falling_edge;

entity registrador_tb is
end registrador_tb;

architecture dataflow of registrador_tb is
  component registrador is
    generic(
      n: natural := 8
    );
    port(
      clock, reset: in bit;
      d: in bit_vector(n-1 downto 0);
      q: out bit_vector(n-1 downto 0)
    );
  end component;

  constant periodoClock : time := 1 ns;
  signal simulando, clk, en, clr : bit := '0';
  signal d, q: bit_vector(3 downto 0);

begin
  -- geração de clock
  clk <= (simulando and (not clk)) after periodoClock/2;

  --! DUT = Design Under Test
  dut: registrador generic map (4) port map (clk, clr, d, q);


  geraEstimulos: process
  begin
    --! habilita geracao de clock
    simulando <= '1';

    -- [bloco de reset]
    clr <= '1';
    wait until falling_edge(clk);
    clr <= '0';
    assert (q="0000")
      report "Saída após o clear não está zerada."
      severity warning;

    -- [blocos de teste]
    -- Note que espera-se a descida do clock para verificar o sinal, para dar
    -- tempo suficiente para a amostragem do registrador (na borda de subida) e
    -- possíveis atrasos (caso considere-se na simulação).
    d <= "0101";
    wait until falling_edge(clk);
    assert (q="0101")
      report "Saída inválida caso 0101."
      severity warning;

    d <= "1010";
    wait until falling_edge(clk);
    assert (q="1010")
      report "Saída inválida caso 1010."
      severity warning;

    d <= "1111";
    wait until falling_edge(clk);
    assert (q="1111")
      report "Saída inválida caso 1010."
      severity warning;

    -- Note que deve-se esperar um pouco neste bloco para o reset assíncrono
    -- produzir seu efeito, mas o tempo é menor que meio período de clock para
    -- comprovar que o reset acontece assíncronamente.
    clr <= '1';
    wait for periodoClock/4;
    clr <= '0';
    assert (q="0000")
      report "Saída clear em operação não está zerada."
      severity warning;

    d <= "1111";
    wait until falling_edge(clk);
    assert (q="1111")
      report "Saída inválida caso 1111."
      severity warning;

    -- parando a geracao de clock
    simulando <= '0';
    -- wait necessário para que o processo não fique rodando para sempre
    wait;
  end process;

end dataflow;
