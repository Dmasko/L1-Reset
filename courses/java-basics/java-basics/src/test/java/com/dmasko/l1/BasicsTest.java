package com.dmasko.l1;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class BasicsTest {
  @Test void maxOfThree_ok() { assertEquals(7, Basics.maxOfThree(7, -1, 3)); }
  @Test void isPrime_ok() { assertTrue(Basics.isPrime(97)); assertFalse(Basics.isPrime(1)); }
  @Test void factorial_ok() { assertEquals(120L, Basics.factorial(5)); }
  @Test void reverse_ok() { assertEquals("cba", Basics.reverse("abc")); }
  @Test void countVowels_ok() { assertEquals(2L, Basics.countVowels("salut")); }
}
