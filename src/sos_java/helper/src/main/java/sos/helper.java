package sos;

import java.util.Map;
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
    public static String getType(Boolean x) {
        return "boolean";
    }
    public static String getType(Byte x) {
        return "byte";
    }
    public static String getType(Short x) {
        return "short";
    }
    public static String getType(Integer x) {
        return "int";
    }
    public static String getType(Long x) {
        return "long";
    }
    public static String getType(Float x) {
        return "float";
    }
    public static String getType(Double x) {
        return "double";
    }
    public static String getType(Character x) {
        return "char";
    }
    public static String getType(String x) {
        return "string";
    }
    public static String getType(Map x) {
        return "map";
    }
    public static String getType(ArrayList x) {
        return "array";
    }
    public static String getType(Table x) {
        return "table";
    }

    public static String printArray(ArrayList x) {
        String s = "";
        for (int i = 0; i < x.size(); i++) {
            s += ("'" + x.get(i) + "',");
        }
        return s;
    }
}
