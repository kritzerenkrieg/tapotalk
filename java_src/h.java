public class h {
    private int a;
    private int b;
    private int c;
    private int d;
    private int e;

    public int a() {
        return this.e & 4095;
    }

    public int b() {
        return this.c & 8191;
    }

    public int c() {
        return this.b & 7;
    }

    public int d() {
        return this.d & 15;
    }

    public int e() {
        return this.a & 255;
    }

    public void f(int var1) {
        this.e = var1 & 4095;
    }

    public void g(int var1) {
        this.c = var1 & 8191;
    }

    public void h(int var1) {
        this.b = var1 & 7;
    }

    public void i(int var1) {
        this.d = var1 & 15;
    }

    public void j(int var1) {
        this.a = var1 & 255;
    }
}