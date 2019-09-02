-------------------------------------------------------
--! @file fa.vhd
--! @brief full adder
--! @author Bruno Albertini (balbertini@usp.br)
--! @date 2019-09-02
-------------------------------------------------------
entity fa is
  port (
    a, b, ci : in  bit;
    r, co : out bit
  );
end entity;

architecture structural of fa is
begin
  r <= a xor b xor ci;
  co <= (a and b) or (a and ci) or (b and ci);
end architecture;
