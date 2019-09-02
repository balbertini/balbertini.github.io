-------------------------------------------------------
--! @file ha.vhd
--! @brief half adder
--! @author Bruno Albertini (balbertini@usp.br)
--! @date 2019-09-02
-------------------------------------------------------
entity ha is
  port (
    a, b : in  bit;
    r, co : out bit
  );
end entity;

architecture structural of ha is
begin
  r <= a xor b;
  co <= (a and b);
end architecture;
