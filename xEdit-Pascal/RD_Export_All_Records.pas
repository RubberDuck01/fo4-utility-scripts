{
  Export list of records
}
unit UserScript;

const
  // skip those records
  sRecordsToSkip = 'TES4,REFR,PGRD,PHZD,ACHR,NAVM,NAVI,LAND';

var
  slExport: TStringList;

function Initialize: integer;
begin
  slExport := TStringList.Create;
end;

function Process(e: IInterface): integer;
begin
  if Pos(Signature(e), sRecordsToSkip) <> 0 then
    Exit;

  slExport.Add(
    GetFileName(e) + ';' +
    IntToHex(FormID(E) AND $FFFFFF, 6) + ';' +
    Signature(e) + ';' + GetElementEditValues(e, 'EDID') + ';' +
    '"' + GetElementEditValues(e, 'FULL')  + '"'
  );
end;

function Finalize: integer;
var
  dlgSave: TSaveDialog;
  ExportFileName: string;
begin
  if slExport.Count <> 0 then begin
    dlgSave := TSaveDialog.Create(nil);
    try
      dlgSave.Options := dlgSave.Options + [ofOverwritePrompt];
      dlgSave.Filter := 'Excel (*.csv)|*.csv';
      dlgSave.InitialDir := ScriptsPath;
      dlgSave.FileName := 'rd_records_export.csv';
      if dlgSave.Execute then begin
        ExportFileName := dlgSave.FileName;
        AddMessage('Saving ' + ExportFileName);
        slExport.SaveToFile(ExportFileName);
      end;
    finally
      dlgSave.Free;
    end;
  end;
  slExport.Free;
end;


end.
