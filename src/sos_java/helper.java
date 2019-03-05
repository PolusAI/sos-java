package sos;

import java.util.Map;

public class helper{  
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
}