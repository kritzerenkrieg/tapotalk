package h0.g;

public class e {
    private int a;
    private int b;
    private int c;

    public int a() {
        return this.c & 8191;
    }

    public int b() {
        return this.a & '\uffff';
    }

    public int c() {
        return this.b & 7;
    }

    public void d(int var1) {
        this.c = var1 & 8191;
    }

    public void e(int var1) {
        this.a = var1 & '\uffff';
    }

    public void f(int var1) {
        this.b = var1 & 7;
    }
}
