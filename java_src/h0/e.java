package h0;

import h0.g.g;
import h0.g.h;
import h0.g.i;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

public class e {
    private final byte[] a = new byte[188];
    private int b = 0;
    private ByteBuffer c = ByteBuffer.allocateDirect(512000);
    private final h0.a d;
    private int e;
    private int f;
    private int g;
    private final List<h0.g.e> h;
    private final List<h> i;
    private boolean j;

    public e() {
        h0.a var1 = new h0.a();
        this.d = var1;
        var1.e(0);
        var1.d(0);
        var1.g(0);
        var1.f(new c());
        this.g = 0;
        this.h = new ArrayList();
        this.i = new ArrayList();
        this.j = false;
    }

    private byte c(byte var1, int var2, int var3) {

        //System.out.println("var1: "+var1+" var2: "+var2+" var3: "+var3+"out: "+(byte)(var1 << var2 | var3));
        return (byte)(var1 << var2 | var3);
    }

    private int d(int var1, int var2, int var3) {
        return var1 << var2 | var3;
    }

    private long e(long var1, int var3, int var4) {
        return var1 << var3 | (long)var4;
    }

    private byte[] f(int var1) {
        return new byte[]{(byte)(var1 >> 24 & 255), (byte)(var1 >> 16 & 255), (byte)(var1 >> 8 & 255), (byte)(var1 & 255)};
    }

    private byte[] g(long var1) {
        return new byte[]{(byte)((int)(var1 >> 56 & 255L)), (byte)((int)(var1 >> 48 & 255L)), (byte)((int)(var1 >> 40 & 255L)), (byte)((int)(var1 >> 32 & 255L)), (byte)((int)(var1 >> 24 & 255L)), (byte)((int)(var1 >> 16 & 255L)), (byte)((int)(var1 >> 8 & 255L)), (byte)((int)(var1 & 255L))};
    }

    private int h(int var1) {
        return var1 + 1 & 15;
    }

    private int i(byte[] var1, int var2, int var3) {
        int var4 = -1;

        for(int var5 = var2; var5 < var2 + var3; ++var5) {
            byte var6 = var1[var5];
            var4 = h0.d.a[(var4 >> 24 ^ var6) & 255] ^ var4 << 8;
        }

        return var4;
    }

    private int j(int var1) {
        if (this.b + var1 > 188) {
            return -4;
        } else {
            byte[] var2 = new byte[var1];
            Arrays.fill(var2, (byte)-1);
            System.arraycopy(var2, 0, this.a, this.b, var1);
            this.b += var1;
            return 0;
        }
    }

    private void o(int var1) {
        System.arraycopy(this.f(this.i(this.a, var1, this.b - var1)), 0, this.a, this.b, 4);
        this.b += 4;
    }

    private void p() {
        int var1 = this.b;
        if (var1 == 188) {
            this.c.put(this.a, 0, var1);
            this.b = 0;
        }
    }

    private void q(int var1, boolean var2, h0.g.c var3) {
        h0.g.a var4 = new h0.g.a();
        var4.l(var1);
        var4.m(0);
        var4.n(0);
        if (var2) {
            var4.q(255);
            var4.r(0);
            var4.p(var3);
        } else {
            var4.q(0);
            var4.r(0);
        }

        if (1 == var1) {
            var4.r(0);
        }

        var4.o(0);
        var4.s(0);
        var4.t(0);
        var4.k(0);
        byte var5 = this.c((byte)0, 0, var4.b());
        byte[] var8 = this.a;
        var1 = this.b;
        var8[var1] = var5;
        this.b = var1 + 1;
        if (var4.b() != 0) {
            var5 = this.c(this.c(this.c(this.c(this.c(this.c(this.c(this.c((byte)0, 0, var4.c()), 1, var4.h()), 1, var4.d()), 1, var4.g()), 1, var4.e()), 1, var4.i()), 1, var4.j()), 1, var4.a());
            var8 = this.a;
            var1 = this.b;
            var8[var1] = var5;
            this.b = var1 + 1;
            if (var2) {
                long var6 = (long)0;
                var5 = (byte)((int)(var4.f().a() >> 25 & 255L | var6));
                var8 = this.a;
                var1 = this.b;
                var8[var1] = var5;
                this.b = var1 + 1;
                System.arraycopy(this.f(this.d((int)(var6 + (var4.f().a() & 33554431L)), 6, var4.f().c()) << 1 | var4.f().b() & 256), 0, this.a, this.b, 4);
                this.b += 4;
                var5 = (byte)(var4.f().b() | 0);
                var8 = this.a;
                var1 = this.b;
                var8[var1] = var5;
                this.b = var1 + 1;
            } else {
                this.j(var4.b() - 1);
            }

        }
    }

    private void s(int var1, int var2, int var3, int var4) {
        h0.g.b var5 = new h0.g.b();
        var5.m(71);
        var5.n(0);
        var5.l(var2);
        var5.o(0);
        var5.k(var1);
        var5.p(0);
        var5.i(var3);
        var5.j(var4);
        System.arraycopy(this.f(this.d(this.d(this.d(this.d(this.d(this.d(this.d(this.d(0, 0, var5.e()), 1, var5.f()), 1, var5.d()), 1, var5.g()), 13, var5.c()), 2, var5.h()), 2, var5.a()), 4, var5.b())), 0, this.a, this.b, 4);
        this.b = 4;
        if (1 == var2 && 1 == var3) {
            this.a[4] = 0;
            this.b = 4 + 1;
        }

    }

    private void t(List<h0.g.e> var1, boolean var2) {
        if (var1 != null && !var1.isEmpty()) {
            h0.g.d var3 = new h0.g.d();
            var3.u(0);
            var3.t(255);
            var3.x(0);
            var3.p(255);
            byte var4;
            byte var5;
            if (var2) {
                var4 = 9;
                var5 = 5;
            } else {
                var4 = 8;
                var5 = 4;
            }

            var3.r(var4 + var1.size() * 4);
            var3.v(1);
            var3.q(255);
            var3.w(0);
            var3.m(255);
            var3.s(0);
            var3.n(0);
            var3.o(var1);
            var3.l(1);
            System.arraycopy(this.g(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(0L, 0, var3.h()), 1, var3.g()), 1, var3.k()), 2, var3.c()), 12, var3.e()), 16, var3.i()), 2, var3.d()), 5, var3.j()), 1, var3.a()), 8, var3.f()), 8, var3.b())), 0, this.a, this.b, 8);
            this.b += 8;

            for(Iterator var6 = var1.iterator(); var6.hasNext(); this.b += 4) {
                h0.g.e var7 = (h0.g.e)var6.next();
                System.arraycopy(this.f(this.d(this.d(this.d(0, 0, var7.b()), 3, var7.c()), 13, var7.a())), 0, this.a, this.b, 4);
            }

            this.o(var5);
            this.j(188 - this.b);
            this.p();
        }

    }

    private void u(int var1, int var2, int var3, int var4, i var5) {
        h0.g.f var6 = new h0.g.f();
        var6.z(1);
        var6.H(var2);
        var6.D(var1);
        var6.x(2);
        var6.F(0);
        var6.E(0);
        var6.u(0);
        var6.s(0);
        var6.y(0);
        var6.G(var3);
        var6.w(0);
        var6.v(0);
        var6.t(0);
        var6.r(0);
        var6.A(0);
        var6.B(0);
        var6.C(var4);
        System.arraycopy(this.g(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(0L, 0, var6.i()), 8, var6.q()), 16, var6.m()), 2, var6.g()), 2, var6.o()), 1, var6.n()), 1, var6.d()), 1, var6.b()), 1, var6.h()), 2, var6.p()), 1, var6.f()), 1, var6.e()), 1, var6.c()), 1, var6.a()), 1, var6.j()), 1, var6.k())), 0, this.a, this.b, 8);
        this.b += 8;
        byte var7 = (byte)(var6.l() | 0);
        byte[] var8 = this.a;
        var1 = this.b;
        var8[var1] = var7;
        this.b = var1 + 1;
        if (2 == var6.p() && 5 == var6.l()) {
            var7 = this.c(this.c(this.c((byte)0, 0, var5.a()), 3, var5.b()), 1, var5.e());
            var8 = this.a;
            var1 = this.b;
            var8[var1] = var7;
            this.b = var1 + 1;
            System.arraycopy(this.f(this.d(this.d(this.d(this.d(0, 0, var5.c()), 1, var5.f()), 15, var5.d()), 1, var5.g())), 0, this.a, this.b, 4);
            this.b += 4;
        }

        if (3 == var6.p() && 10 == var6.l()) {
            var5.h(3);
            var7 = this.c(this.c(this.c((byte)0, 0, var5.a()), 3, var5.b()), 1, var5.e());
            byte[] var10 = this.a;
            var1 = this.b;
            var10[var1] = var7;
            this.b = var1 + 1;
            System.arraycopy(this.f(this.d(this.d(this.d(this.d(0, 0, var5.c()), 1, var5.f()), 15, var5.d()), 1, var5.g())), 0, this.a, this.b, 4);
            this.b += 4;
        }

        if (224 == var2 && 27 == this.d.c().c().get(this.f).d()) {
            byte[] var9 = this.a;
            var1 = this.b;
            var9[var1] = 0;
            ++var1;
            this.b = var1;
            var9[var1] = 0;
            ++var1;
            this.b = var1;
            var9[var1] = 0;
            ++var1;
            this.b = var1;
            var9[var1] = 1;
            ++var1;
            this.b = var1;
            var9[var1] = 9;
            ++var1;
            this.b = var1;
            var9[var1] = -16;
            this.b = var1 + 1;
        }

    }

    private void v(List<h> var1, int var2, boolean var3) {
        if (var1 != null && !var1.isEmpty()) {
            g var4 = new g();
            var4.D(2);
            var4.C(1);
            var4.F(0);
            var4.w(255);
            byte var5;
            byte var6;
            if (var3) {
                var5 = 13;
                var6 = 5;
            } else {
                var5 = 12;
                var6 = 4;
            }

            var4.A(var5 + var1.size() * 5);
            var4.v(var2);
            var4.x(255);
            var4.E(0);
            var4.q(255);
            var4.B(0);
            var4.r(0);
            var4.y(255);
            var4.s(256);
            var4.z(255);
            var4.u(0);
            var4.t(var1);
            var4.p(1);
            System.arraycopy(this.g(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(this.e(0L, 0, var4.m()), 1, var4.l()), 1, var4.o()), 2, var4.f()), 12, var4.j()), 16, var4.e()), 2, var4.g()), 5, var4.n()), 1, var4.a()), 8, var4.k()), 8, var4.b())), 0, this.a, this.b, 8);
            this.b += 8;
            System.arraycopy(this.f(this.d(this.d(this.d(this.d(0, 0, var4.h()), 13, var4.c()), 4, var4.i()), 12, var4.d())), 0, this.a, this.b, 4);
            this.b += 4;

            for(Iterator var9 = var1.iterator(); var9.hasNext(); this.b += 4) {
                h var7 = (h)var9.next();
                byte var8 = this.c((byte)0, 0, var7.e());
                byte[] var10 = this.a;
                var2 = this.b;
                var10[var2] = var8;
                this.b = var2 + 1;
                System.arraycopy(this.f(this.d(this.d(this.d(this.d(0, 0, var7.c()), 13, var7.b()), 4, var7.d()), 12, var7.a())), 0, this.a, this.b, 4);
            }

            this.o(var6);
            this.j(188 - this.b);
            this.p();
        }

    }

    public void a(int var1, int var2) {
        this.d.c().g(var1);
        this.d.c().f(0);
        this.d.c().h(0);
        this.d.c().i(var2);
    }

    public void b(int var1, f_enum var2) {
        b var3 = new b();
        var3.g(var1);
        var3.f(0);
        var1 = var2.ordinal() + 1; // edit
        //var1 = null.a[var2.ordinal()];
        if (var1 != 1) {
            if (var1 != 2) {
                if (var1 != 3) {
                    if (var1 == 4) {
                        var3.h(192);
                        var3.e(17);
                        var3.i(144);
                        this.e = this.d.c().c().size();
                    }
                } else {
                    var3.h(192);
                    var3.e(17);
                    var3.i(15);
                    this.e = this.d.c().c().size();
                }
            } else {
                var3.h(224);
                var3.e(18);
                var3.i(27);
                this.f = this.d.c().c().size();
            }
        } else {
            var3.h(224);
            var3.e(18);
            var3.i(36);
            this.f = this.d.c().c().size();
        }

        var1 = this.d.c().d();
        this.d.c().h(var1 + 1);
        this.d.c().c().add(var3);
    }

    public byte[] k(byte[] var1, int var2, long var3) {
        if (var1 == null) {
            return null;
        } else {
            byte[] var5 = var1;
            if (var1.length > var2) {
                var5 = Arrays.copyOf(var1, var2);
            }

            this.n();
            this.a(66, 1);
            f_enum var6 = f_enum.MUXTS_CODEC_PCMA;
            //f_original var6 = f_original.z;
            this.b(68, var6);
            this.r(var5, var3, var6);
            return this.l();
        }
    }

    public byte[] l() {
        this.c.flip();
        int var1 = this.c.remaining();
        if (var1 > 0) {
            byte[] var2 = new byte[var1];
            this.c.get(var2);
            return var2;
        } else {
            return null;
        }
    }

    public void m() {
        this.c = null;
    }

    public void n() {
        this.b = 0;
        this.c.clear();
        this.d.e(0);
        this.d.d(0);
        this.d.g(0);
        this.d.f(new c());
        this.g = 0;
        this.h.clear();
        this.i.clear();
    }

    public void r(byte[] var1, long var2, f_enum var4) {
        if (var1 != null) {
            int var5;
            int var6;
            int var7;
            int var8;
            int var9;
            boolean var14;
            label81: {
                label92: {
                    var5 = var1.length;
                    if (f_enum.MUXTS_CODEC_HEVC != var4 && f_enum.MUXTS_CODEC_AVC != var4) {
                        if (f_enum.MUXTS_CODEC_AAC == var4) {
                            var6 = this.e;
                            var7 = var5 + 8;
                            break label92;
                        }

                        if (f_enum.MUXTS_CODEC_PCMA != var4) {
                            var14 = false;
                            var7 = 0;
                            var8 = 0;
                            var9 = 0;
                            break label81;
                        }

                        var7 = this.e;
                    } else {
                        var7 = this.f;
                    }

                    var6 = var7;
                    var7 = var5;
                }

                boolean var10 = false;
                byte var11 = 0;
                var9 = var6;
                var8 = var7;
                var7 = var11;
                var14 = var10;
            }

            while(true) {
                while(var5 > 0) {
                    b var13;
                    int var15;
                    if (this.g == 0) {
                        h0.g.e var12 = new h0.g.e();
                        var12.e(this.d.c().e());
                        var12.d(this.d.c().b());
                        var12.f(255);
                        this.h.add(var12);

                        for(var15 = 0; var15 < this.d.c().d(); ++var15) {
                            h var16 = new h();
                            var13 = (b)this.d.c().c().get(var15);
                            var16.g(var13.b());
                            var16.j(var13.d());
                            var16.f(0);
                            var16.h(255);
                            var16.i(255);
                            this.i.add(var16);
                        }
                    }

                    if (this.g % 64 == 0) {
                        this.s(this.d.b(), 1, 1, this.d.a());
                        this.t(this.h, true);
                        var15 = this.h(this.d.a());
                        this.d.d(var15);
                        ++this.g;
                        this.s(this.d.c().b(), 1, 1, this.d.c().a());
                        this.v(this.i, this.d.c().e(), true);
                        var15 = this.h(this.d.c().a());
                        this.d.c().f(var15);
                        ++this.g;
                    } else {
                        b var17;
                        if (var14) {
                            var17 = (b)this.d.c().c().get(var9);
                            byte[] var20;
                            if (var5 >= 184) {
                                this.s(var17.b(), 0, 1, var17.a());
                                var20 = this.a;
                                var15 = this.b;
                                System.arraycopy(var1, var7, var20, var15, 188 - var15);
                                var15 = this.b;
                                var5 -= 188 - var15;
                                this.b = var15 + (188 - var15);
                                var7 += 188 - var15;
                            } else {
                                this.s(var17.b(), 0, 3, var17.a());
                                this.q(188 - var5 - 5, false, new h0.g.c());
                                var20 = this.a;
                                var15 = this.b;
                                System.arraycopy(var1, var7, var20, var15, 188 - var15);
                                var15 = this.b;
                                var7 += 188 - var15;
                                var5 -= 188 - var15;
                                this.b = var15 + (188 - var15);
                            }

                            var17.f(this.h(var17.a()));
                            ++this.g;
                            this.p();
                        } else {
                            var17 = (b)this.d.c().c().get(var9);
                            this.s(var17.b(), 1, 3, var17.a());
                            h0.g.c var18 = new h0.g.c();
                            var18.d(var2);
                            var18.f(255);
                            var18.e(0);
                            if (this.j) {
                                this.q(7, true, var18);
                            } else if (f_enum.MUXTS_CODEC_AAC != var4 && f_enum.MUXTS_CODEC_PCMA != var4) {
                                this.q(7, true, var18);
                            } else {
                                this.q(1, false, var18);
                            }

                            i var19 = new i();
                            var19.h(2);
                            var19.l(255);
                            var19.m(255);
                            var19.n(255);
                            var19.i((int)(var2 >> 30));
                            System.out.println("asi clock reference: ");
                            System.out.println((int)(var2 >> 30));
                            var19.j((int)(var2 >> 15));
                            System.out.println((int)(var2 >> 15));
                            System.out.println();
                            System.out.println(var19.getD());
                            System.out.println(var19.getF());
                            System.out.println();
                            var19.k((int)var2);
                            var13 = (b)this.d.c().c().get(var9);
                            this.u(var8, var13.c(), 2, 5, var19);
                            var13.f(this.h(var13.a()));
                            ++this.g;
                            var6 = this.b;
                            if (var5 >= 188 - var6) {
                                System.arraycopy(var1, var7, this.a, var6, 188 - var6);
                                var6 = this.b;
                                var7 += 188 - var6;
                                var5 -= 188 - var6;
                                this.b = var6 + (188 - var6);
                            }

                            this.p();
                            var14 = true;
                        }
                    }
                }

                return;
            }
        }
    }
}