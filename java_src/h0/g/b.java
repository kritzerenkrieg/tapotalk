package h0.g;

public class b {
    private int a;
    private int b;
    private int c;
    private int d;
    private int e;
    private int f;
    private int g;
    private int h;

    public int a() {
        return this.g & 3;
    }

    public int b() {
        return this.h & 15;
    }

    public int c() {
        return this.e & 8191;
    }

    public int d() {
        return this.c & 1;
    }

    public int e() {
        return this.a & 255;
    }

    public int f() {
        return this.b & 1;
    }

    public int g() {
        return this.d & 1;
    }

    public int h() {
        return this.f & 3;
    }

    public void i(int var1) {
        this.g = var1 & 3;
    }

    public void j(int var1) {
        this.h = var1 & 15;
    }

    public void k(int var1) {
        this.e = var1 & 8191;
    }

    public void l(int var1) {
        this.c = var1 & 1;
    }

    public void m(int var1) {
        this.a = var1 & 255;
    }

    public void n(int var1) {
        this.b = var1 & 1;
    }

    public void o(int var1) {
        this.d = var1 & 1;
    }

    public void p(int var1) {
        this.f = var1 & 3;
    }
}
