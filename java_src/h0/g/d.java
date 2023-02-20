package h0.g;

import java.util.ArrayList;
import java.util.List;

public class d {
    private int a;
    private int b;
    private int c;
    private int d;
    private int e;
    private int f;
    private int g;
    private int h;
    private int i;
    private int j;
    private int k;
    private List<e> l = new ArrayList();
    private int m;

    public int a() {
        return this.i & 1;
    }

    public int b() {
        return this.k & 255;
    }

    public int c() {
        return this.d & 3;
    }

    public int d() {
        return this.g & 3;
    }

    public int e() {
        return this.e & 4095;
    }

    public int f() {
        return this.j & 255;
    }

    public int g() {
        return this.b & 1;
    }

    public int h() {
        return this.a & 255;
    }

    public int i() {
        return this.f & '\uffff';
    }

    public int j() {
        return this.h & 31;
    }

    public int k() {
        return this.c & 1;
    }

    public void l(int var1) {
        this.m = var1 & -1;
    }

    public void m(int var1) {
        this.i = var1 & 1;
    }

    public void n(int var1) {
        this.k = var1 & 255;
    }

    public void o(List<e> var1) {
        this.l = var1;
    }

    public void p(int var1) {
        this.d = var1 & 3;
    }

    public void q(int var1) {
        this.g = var1 & 3;
    }

    public void r(int var1) {
        this.e = var1 & 4095;
    }

    public void s(int var1) {
        this.j = var1 & 255;
    }

    public void t(int var1) {
        this.b = var1 & 1;
    }

    public void u(int var1) {
        this.a = var1 & 255;
    }

    public void v(int var1) {
        this.f = var1 & '\uffff';
    }

    public void w(int var1) {
        this.h = var1 & 31;
    }

    public void x(int var1) {
        this.c = var1 & 1;
    }
}