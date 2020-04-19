using System;
using System.Data;
using System.Data.SqlClient;
using System.Data.SqlTypes;
using Microsoft.SqlServer.Server;
using System.Text;
using System.IO;

[Serializable]
[SqlUserDefinedAggregate(Format.UserDefined, MaxByteSize = 8000)]
public class AvgAge : IBinarySerialize
{
    //private StringBuilder intermediateResult;       // Intermidiate result
    private int intermediateResult;
    private int count;

    public void Init()
    {
        intermediateResult = 0;
        count = 0;
    }

    public void Accumulate(SqlInt32 Value)
    {
        if (Value.IsNull)
        {
            return;
        }
        //intermediateResult.Append(Value.Value).Append(',');
        intermediateResult += Value.Value;
        count++;
    }

    public void Merge(AvgAge other)
    {
        intermediateResult += (other.intermediateResult);
        count += (other.count);
    }

    public SqlInt32 Terminate()
    {
        int res = intermediateResult / count;        
        return res;
    }

    public void Read(BinaryReader r)
    {
        intermediateResult = Int32.Parse(r.ReadString());
        count++;
    }

    public void Write(BinaryWriter w)
    {
        w.Write((intermediateResult / count).ToString());
    }
}
