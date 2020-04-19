program lab8;

{$APPTYPE CONSOLE}

uses
  SysUtils;


{$L PPSTART.OBJ}
{$L SETCLER.OBJ}
{$L COUNT.OBJ}
{$L A-B.OBJ}

PROCEDURE START; EXTERNAL;

begin
  ASM
    CALL START;
  END;
end.









