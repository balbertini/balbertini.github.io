-------------------------------------------------------
--! @file ffd.vhd
--! @brief Flip-flop tipo D com reset assincrono
--! @author Bruno Albertini (balbertini@usp.br)
--! @date 2019-09-02
-------------------------------------------------------
library ieee;
use ieee.numeric_bit.rising_edge;

entity ffd is
  port (
    clock, d, reset: in bit;
    q: out bit
  );
end entity;

architecture processor of ffd is
begin
  sequencial: process(clock, reset)
  begin
    if reset='1' then
      q <= '0';
    elsif rising_edge(clock) then
      q <= d;
    end if;
  end process;
end architecture;
