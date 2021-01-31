entity A is
  port (
    entradaA: in bit;
    saidaA: out bit
  );
end entity;
architecture arch of A is
begin
  saidaA <= not(entradaA);
end architecture;

entity B is
  port (
    entradaB: in bit_vector(1 downto 0);
    saidaB: out bit_vector(1 downto 0)
  );
end entity;
architecture arch of B is
  component A is
    port (
      entradaA: in bit;
      saidaA: out bit
    );
  end component;
begin
  not1: A port map (entradaB(0), saidaB(0));
  not2: A port map (entradaB(1), saidaB(1));
end architecture;
