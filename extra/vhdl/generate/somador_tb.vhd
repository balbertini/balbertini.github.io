-------------------------------------------------------
--! @file somador_tb.vhd
--! @brief Testenbench para o somador com generate
--! @author Bruno Albertini (balbertini@usp.br)
--! @date 2019-09-02
-------------------------------------------------------
entity somador_tb is
end entity somador_tb;

architecture comportamental of somador_tb is
  component somador is
    generic(
      bits: natural
    );
    port(
      a,b: in  bit_vector(bits-1 downto 0);
      s:   out bit_vector(bits-1 downto 0);
      co:  out bit
    );
  end component;

  signal a : bit_vector (3 downto 0);
  signal b : bit_vector (3 downto 0);
  signal sum : bit_vector (3 downto 0);
  signal cout : bit;
begin
  som: somador generic map(4) port map(a,b,sum,cout);

  st: process is
    type pattern_type is record
      a : bit_vector (3 downto 0);
      b : bit_vector (3 downto 0);
      sum : bit_vector (3 downto 0);
      cout : bit;
    end record;

    type pattern_array is array (natural range <>) of pattern_type;
    constant patterns : pattern_array :=
      (("0000","1111","1111",'0'),
       ("1010","0001","1011",'0'),
       ("1110","0010","0000",'1'),
       ("1001","0011","1100",'0'));
  begin
    for k in patterns'range loop
      a <= patterns(k).a;
      b <= patterns(k).b;

      wait for 1 ns;

      assert sum = patterns(k).sum
        report "Teste falhou (soma)." severity error;

      assert cout = patterns(k).cout
        report "Teste falhou (cout)." severity error;
    end loop;

    wait;
  end process;
end comportamental;
