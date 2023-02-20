package h0.g;

public class c {
    private long a;
    private int b;
    private int c;

    public long a() {
        return this.a & 8589934591L;
    }

    public int b() {
        return this.c & 511;
    }

    public int c() {
        return this.b & 63;
    }

    public void d(long var1) {
        this.a = var1 & 8589934591L;
    }

    public void e(int var1) {
        this.c = var1 & 511;
    }

    public void f(int var1) {
        this.b = var1 & 63;
    }
}

