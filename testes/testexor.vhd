entity minhaentidade is
  port (
    a: in bit_vector(7 downto 0);
    s: out bit_vector(7 downto 0)
  );
end entity;

architecture arch of minhaentidade is
  signal temp: bit_vector(7 downto 0);
begin
  cadeia_de_nands: for i in 1 to 7 generate
    temp(i-1) <= a(i) nand temp(i-1);
  end generate;

end architecture;
