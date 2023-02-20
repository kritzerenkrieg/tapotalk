package g0;

public class a {
    private static final short[] a = new short[]{255, 511, 1023, 2047, 4095, 8191, 16383, 32767};
    private static final short[] b = new short[]{63, 127, 255, 511, 1023, 2047, 4095, 8191};

    public static byte[] a(byte[] var0, int var1) {
        byte[] var2 = new byte[var1 << 1];

        for(int var3 = 0; var3 < var1; ++var3) {
            short var4 = c(var0[var3]);
            int var5 = var3 * 2;
            var2[var5] = (byte)var4;
            var2[var5 + 1] = (byte)(var4 >> 8);
        }

        return var2;
    }

    public static byte[] b(byte[] var0, int var1) {
        int var2 = var1 / 2;
        byte[] var3 = new byte[var2];

        for(var1 = 0; var1 < var2; ++var1) {
            int var4 = var1 * 2;
            byte var5 = var0[var4];
            var3[var1] = d((short) (((var0[var4 + 1] & 255) << 8) | (var5 & 255)));
        }

        return var3;
    }

    private static short c(byte var0) {
        byte var1 = (byte)(var0 ^ 85);
        short var2 = (short)((var1 & 15) << 4);
        short var4 = (short)((var1 & 112) >> 4);
        int var5;
        if (var4 != 0) {
            if (var4 != 1) {
                var5 = (short)(var2 + 264) << var4 - 1;
            } else {
                var5 = var2 + 264;
            }
        } else {
            var5 = var2 + 8;
        }

        short var3 = (short)var5;
        if ((var1 & 128) == 0) {
            var3 = (short)(-var3);
        }

        return var3;
    }

    private static byte d(short var0) {
        short var1;
        if (var0 >= 0) {
            var1 = 213;
        } else {
            byte var2 = 85;
            short var3 = (short)(-var0 - 1);
            var1 = var2;
            var0 = var3;
            if (var3 < 0) {
                var0 = 32767;
                var1 = var2;
            }
        }

        short var5 = e(var0, a, (short)8);
        int var6;
        if (var5 >= 8) {
            var6 = var1 ^ 127;
        } else {
            char var4 = (char)(var5 << 4);
            int var7;
            if (var5 < 2) {
                var7 = var0 >> 4;
            } else {
                var7 = var0 >> var5 + 3;
            }

            var6 = (char)(var7 & 15 | var4) ^ var1;
        }

        return (byte)var6;
    }

    private static short e(short var0, short[] var1, short var2) {
        for(short var3 = 0; var3 < var2; ++var3) {
            if (var0 <= var1[var3]) {
                return var3;
            }
        }

        return var2;
    }

    public static byte[] f(short[] var0) {
        int var1 = var0.length;
        byte[] var2 = new byte[var1 << 1];

        for(int var3 = 0; var3 < var1; ++var3) {
            int var4 = var3 * 2;
            var2[var4] = (byte)var0[var3];
            var2[var4 + 1] = (byte)(var0[var3] >> 8);
        }

        return var2;
    }
}

