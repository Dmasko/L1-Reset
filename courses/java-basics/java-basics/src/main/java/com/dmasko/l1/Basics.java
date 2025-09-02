package com.dmasko.l1;

public final class Basics {
  private Basics() {}
  public static int maxOfThree(int a, int b, int c) { return Math.max(a, Math.max(b, c)); }
  public static boolean isPrime(int n) {
    if (n < 2) return false;
    if (n % 2 == 0) return n == 2;
    for (int i = 3; i * i <= n; i += 2) if (n % i == 0) return false;
    return true;
  }
  public static long factorial(int n) {
    if (n < 0) throw new IllegalArgumentException("n<0");
    long r = 1; for (int i=2;i<=n;i++) r *= i; return r;
  }
  public static String reverse(String s) { return new StringBuilder(s).reverse().toString(); }
  public static long countVowels(String s) {
    if (s == null) return 0;
    long c = 0; for (char ch : s.toLowerCase().toCharArray())
      if ("aeiouy".indexOf(ch) >= 0) c++;
    return c;
  }
}
