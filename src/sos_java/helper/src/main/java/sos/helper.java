package sos;

import java.util.Map;
import java.util.Iterator;
import java.util.ArrayList;
import static tech.tablesaw.aggregate.AggregateFunctions.*;
import tech.tablesaw.api.*;
import tech.tablesaw.columns.*;

/**
 * Helper class for reflecting and specialized printing
 * Used by sos-java Python package on top of IJava Jupyter kernel
 *
 */
public class helper 
{
    /**
     * Type reflection method.
     * 
     * <p> This function reflects types of objects supported across SoS: numerical types, arrays, hash maps and dataframes.
     * This function uses standard reflection mechanism in Java. 
     * Primitive types are automatically converted to a corresponding object wrapper classes (https://docs.oracle.com/javase/tutorial/java/data/autoboxing.html)
     * 
     */
    public static String getType(Object x){
        return x.getClass().getSimpleName();
    }

    /**
     * ArrayList prinitng to string. Elements are shielded with quotes.
     */
    public static String printArray(ArrayList x) {
        String s = "";
        for (int i = 0; i < x.size(); i++) {
            s += ("'" + x.get(i) + "',");
        }
        return s;
    }

    /**
     * Method for getting the first element in the HashMap for type reflection of keys and values.
     */
    public static Map.Entry elementMap(Map mp) {
        String s = "";
        Iterator it = mp.entrySet().iterator();
        return (Map.Entry)it.next();
    }

    /**
     * HashMap's key type reflection.
     */
    public static String getMapKeyType(Map mp) {
        return helper.getType(elementMap(mp).getKey());
    }

    /**
     * HashMap's value type reflection.
     */
    public static String getMapValueType(Map mp) {
        return helper.getType(elementMap(mp).getValue());
    }

    /**
     * HashMap prinitng to string in Python dict format. Elements are shielded with quotes.
     */
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
