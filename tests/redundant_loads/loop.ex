( (main (x)
  (0  (ld r1 x)
      (br r1 1 2) )
  (1  (sub r1 r1 r1)
      (br r1 1 2) )
  (2  (ret r1) ) ) )
