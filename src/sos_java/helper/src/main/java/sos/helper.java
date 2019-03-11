package sos;

import java.util.Map;
import java.util.Iterator;
import java.util.ArrayList;
import static tech.tablesaw.aggregate.AggregateFunctions.*;
import tech.tablesaw.api.*;
import tech.tablesaw.columns.*;

/**
 * Helper class for SoS notebooks
 * getType(var) returns variable type through polymorhism
 *
 */
public class helper 
{
    public static String getType(Object x){
        return x.getClass().getSimpleName();
    }

    public static String printArray(ArrayList x) {
        String s = "";
        for (int i = 0; i < x.size(); i++) {
            s += ("'" + x.get(i) + "',");
        }
        return s;
    }

    public static Map.Entry elementMap(Map mp) {
        String s = "";
        Iterator it = mp.entrySet().iterator();
        return (Map.Entry)it.next();
    }

    public static String getMapKeyType(Map mp) {
        return helper.getType(elementMap(mp).getKey());
    }

    public static String getMapValueType(Map mp) {
        return helper.getType(elementMap(mp).getValue());
    }

    public static String printMap(Map mp) {
        Iterator entries = mp.entrySet().iterator();
        String s = "";
        while (entries.hasNext()) {
            Map.Entry entry = (Map.Entry) entries.next();
            s += ("\"" + entry.getKey() + "\": \"" + entry.getValue() + "\", ");
        }
        return ("{" + s + "}");
    }
}
