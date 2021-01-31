-------------------------------------------------------
--! @file ffd.vhd
--! @brief Flip-flop tipo D com reset assincrono
--! @author Bruno Albertini (balbertini@usp.br)
--! @date 2019-09-02
-------------------------------------------------------
entity registrador is
  generic(
    n: natural := 8
  );
  port(
    clock, reset: in bit;
    d: in bit_vector(n-1 downto 0);
    q: out bit_vector(n-1 downto 0)
  );
end entity;

architecture arch of registrador is
  component ffd is
    port (
      clock, d, reset: in bit;
      q: out bit
    );
  end component;
begin
  regs: for i in n-1 downto 0 generate
    ffs: ffd port map(clock, d(i), reset, q(i));
  end generate;
end architecture;
