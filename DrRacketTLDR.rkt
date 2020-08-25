;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-advanced-reader.ss" "lang")((modname KlausurRacket) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #t #t none #f () #f)))
(printf "(V0.2) DrRacketBible, everything except homework programs are in this file. Might take some time to run through all of the tests. ")
(newline)
(define delta 0.01)

;;DRRACKET KLAUSUR VORBEREITUNG
;;THEMEN
;;0.Strukturen/Definitionen
;;1.Rekursion/local
;;2.foldr /foldl
;;3.map/filter
;;4.akkumulator

;;5.lambda
;;###########################;;
;;#
;;# 0. INTRO/VERZEICHNIS
;;# 1. USEFUL FUNCTIONS
;;# 2. KLAUSURTHEMEN
;;# 3. ÜBUNGEN
;;# 4. KLAUSURÜBUNGEN
;;#
;;###########################;;

;;##################################################################################;;
;;#11111111111111111111111111111111111111111111111111111111111111111111111111111111#;;
;;#11111111111111111111111111111111111111111111111111111111111111111111111111111111#;;
;;#11111111111111111111111111111111111111111111111111111111111111111111111111111111#;;
;;##################################################################################;;

;; BONUS XXX FUNCTIONS XXX
;; (reverse lst) -> reverses list
;; (length lst) -> length of the list
;; (append lst lst lst ...) -> joins lists into one list!
;; (error 'functionname "error message")
;; (sort lst argument) (sort '(2 3 1) >) -> '(3 2 1)
;; (floor num) -> rundet down 3.5 -> 3

;; BLANK TESTS
;; (check-expect test expected)
;; (check-within test expected delta)
;; (check-error 'function "message")

;; VERY USEFUL ABSTRACT FUNCTIONS

;; FILTER FOR ALL OF YOUR NEEDS!
(define (filteris test lst)
  (cond
    [(empty? lst) empty]
    [(test (first lst)) (cons (first lst) (filteris test (rest lst)))]
    [else (filteris test (rest lst))]
    ))
(check-expect (filteris even? '(1 2 3 4 5 6)) '(2 4 6))

;; LIST LENGTH CALCULATOR!
(define (listlength lst)
  (cond
    [(empty? lst) 0]
    [else (+ (listlength (rest lst)) 1)]))

;; JOIN TWO LISTS INTO ONE LIST!
(define (addlist lst1 lst2)
  (cond
    [(or (empty? lst1)
         (empty? lst2))
         empty]
    [else (cons
           (+ (first lst1) (first lst2))
           (addlist (rest lst1) (rest lst2)))]))

;; INSERT NUMBER IN THE BELONGING POSITION IN THE LIST
(define (insertanumber a lst)
  (cond
    [(empty? lst) (cons a empty)]
    [else
     (cond
       [(<= a (first lst)) (cons a lst)]
       [(> a (first lst)) (cons (first lst) (insertanumber a (rest lst)))])]))

;; SUM ALL NUMBERS IN THE LIST!
(define (sumofnum lst)
  (cond
    [(empty? lst) 0]
    [else (+
           (first lst)
           (sumofnum (rest lst)))]))

;; SUCC AND PRED!
(define (succ a)
  (if (>= a 0) (+ a 1) 0)) ;; If a >= 0, then add +1 to a, else 0.
(define (pred a)
  (if (> a 0) (- a 1) 0)) ;; If a > 0, then take -1 from a, else 0.

;; SORT NUMBERS LIST!
(define (sorty op lst)
  (cond [(empty? lst) empty]
        [else (inserty op (first lst) (sorty op (rest lst)))]
        ))

(define (inserty op n lst2)
  (cond [(empty? lst2) (cons n empty)]
        [(op n (first lst2)) (cons n lst2)]
        [else (cons (first lst2) (inserty op n (rest lst2)))]
        ))

;; FILTER EVEN NUMBERS OF A LIST! TWO OPTIONS
(define (evennums lst)
  (cond [(empty? lst) empty]
        [(= 1 (modulo (first lst) 2)) (evennums (rest lst))]
        [else (cons (first lst) (evennums (rest lst)))]
        ))
(define nums '(1 2 3 4 54 5 5 5 6 76 7 3 3 21 2))
(filter even? nums)

;;##################################################################################;;
;;#22222222222222222222222222222222222222222222222222222222222222222222222222222222#;;
;;#22222222222222222222222222222222222222222222222222222222222222222222222222222222#;;
;;#22222222222222222222222222222222222222222222222222222222222222222222222222222222#;;
;;##################################################################################;;

;; 0.1 Strukturen
(define-struct point (x y))
(define pointA (make-point 0 10)) ;;KONSTRUKTOR
;; (point? pointA)-> true PRÄDIKAT
;; (point-x pointA)-> 0 SELEKTOR

;; 0.2 Definitionen
;; (define (nameofthefunction parameter1 parameter2 parametern-1) whatdoesitdo?)

;; 1.1 STRUKTURELLE REKURSION T03 
;; simple recursion to find out if a symbol is in the list!
(define animals '(dog cat cow horse snake))
(define cars '(bmw opel audi mercedes pagani skoda))
(define (inlist? symbol list)
  (cond
    [(empty? list) "Symbol/word not in the list."]
    [(symbol=? (first list) symbol)  "Symbol/word is in the list."]
    [else (inlist? symbol (rest list))]))
(check-expect (inlist? 'mercedes cars) "Symbol/word is in the list.")

(define (sum list)
  (cond
    [(empty? list) 0]
    [else (+ (first list)
             (sum (rest list)))]))
(define numbers '(1 2 3 4 5 6 7 8 9 10))
(define randomnumbers '(1 2 3 8 48 2 0 3 5 8 9 1))
(check-expect (sum numbers) 55)

(define (fib x)
  (cond
    [(= x 0) 0]
    [(= x 1) 1]
    [else (+ (fib (- x 1))
             (fib (- x 2)))]))
(check-expect (fib 10) 55)

(define (appendlists list1 list2)
  (cond
    [(empty? list1) list2]
    [else (cons (first list1) (appendlists (rest list1) list2))]))

(define (addlists list1 list2)
  (cond
    [(empty? list1) empty]
    [(empty? list2) empty]
    [else (cons (+ (first list1) (first list2))
                (addlists (rest list1) (rest list2)))]))
(check-expect (addlists numbers randomnumbers) '(2 4 6 12 53 8 7 11 14 18))

(define (pickfromlist list n)
  (cond
    [(empty? list) (error 'pickfromlist "list is empty or too short!")]
    [(= n 1) (first list)]
    [(> n 1) (pickfromlist (rest list) (- n 1))]))
(check-expect (pickfromlist cars 3) 'audi)

;; 1.2 LOCAL FUNCTIONS T04
;; easy Beispiel
(define (f x y z)
  (local( ;; local block opened
         (define (square z) (* z z)) ;;benutzt z von square function
         (define (plusysqr q) (square (+ q y))) ;;benutzt q von plusysqr und y von f oben!
         ) ;; local block closed
(+ (plusysqr x) (plusysqr z))))

;; 3.1 foldl/foldr allgemein
;; foldl fängt hinten an und geht nach links
;; foldr fängt links an und geht nach rechts
;; foldl für umdrehen
;; foldr für summieren

;; (foldl procedure initialvalue list)
;; (foldl + 0 numbers) -> 55

(check-expect (foldl cons empty '(1 2 3)) '(3 2 1))
(check-expect (foldr cons empty '(1 2 3)) '(1 2 3))


;;T02 RATIONAL NUMBERS EXAMPLE
(define-struct rat (numerator denominator))
;; mul-rat: rat rat -> rat
;; multiplies two rat structures into one
;; EXAMPLE: (mulrat (make-rat 1 2) (make-rat 3 5)) -> (make-rat 3 10)
(define (mulrat x y)
  (make-rat (* (rat-numerator x) (rat-numerator y))
            (* (rat-denominator x) (rat-denominator y))))
(check-expect (mulrat (make-rat 1 2) (make-rat 3 5)) (make-rat 3 10))

;; add-rat: rat rat -> rat
;; adds two rat structures with eachother
;; EXAMPLE: (addrat (make-rat 1 2) (make-rat 2 4)) ->
(define (addrat x y)
  (make-rat (+ (* (rat-numerator x) (rat-numerator y))
               (* (rat-denominator x) (rat-denominator y)))
            (* (rat-denominator x) (rat-denominator y))))
(check-expect (addrat (make-rat 1 2) (make-rat 3 5)) (make-rat 13 10))

;; print-rat: rat -> String
;; prints rat structure as a string!
(define (printrat x)
  (string-append (number->string (rat-numerator x)) "/" (number->string(rat-denominator x))))
(define onethrid (make-rat 1 3))
(check-expect (printrat onethrid) "1/3")


;; COND EXAMPLE
(define (distanceto0 x)
  (cond
    [(number? x) x]
    [(point? x) (sqrt (+ (sqr (point-x x)) (sqr (point-y x))))]
    [else "not a point/number"]))

;;##################################################################################;;
;;#33333333333333333333333333333333333333333333333333333333333333333333333333333333#;;
;;#33333333333333333333333333333333333333333333333333333333333333333333333333333333#;;
;;#33333333333333333333333333333333333333333333333333333333333333333333333333333333#;;
;;##################################################################################;;

;; ÜBUNG01
;; 4. Tetraedervolumen
;; volume: num -> num
;; calculates the volume of a tetreader given its side length a.
(define (volume a)
  (* k (pow3 a)))
(define (pow3 x) ;; calculates x^3
  (* x x x))
(define k (/ (sqrt 2) 12)) ;; calculates fuckfest sqrt2/12

;; 6. Steuern
;; get-taxrate: num -> num
;; calculates income tax based on given income. rounds down.
(define (get-taxrate income)
  (floor (* income 0.0005)))
;; NOT DONE !!!

;; ÜBUNG02
;; 3. Rekursion
;; euclid: num num -> num
;; calculates ggT of a and b
(define (euclid a b)
  (cond
    [(= a 0) b]
    [(= b 0) a]
    [(> a b) (euclid (- a b) b)]
    [else (euclid a (- b a))]
    ))
(check-expect (euclid 0 3) 3)
(check-expect (euclid 12 18) 6)
(check-expect (euclid 1071 1029) 21)

;; 5. Listen
;; calulate the length of the list
;; calculates length of any given list no matter what it contains. thats abstract.
(define (my-len lst) ;; length is implemented naturally already so save it boi.
  (cond
    [(empty? lst) 0]
    [else (+ (my-len (rest lst)) 1)]))
;; go through a list and looks if given symbol is in it.
(define (contains? lst sym)
  (cond
    [(empty? lst) false]
    [(symbol=? sym (first lst)) true]
    [else (contains? (rest lst) sym)]))
(check-expect (contains? '(a b c) 'c) true)
(check-expect (contains? '(a b c) 'd) false)
(check-expect (contains? empty 'x) false)
;; remove duplicates from a list!
(define (removedupes lst)
  (cond
    [(empty? lst) lst]
    [(contains? (rest lst) (first lst)) (removedupes (rest lst))]
    [else (cons (first lst) (removedupes (rest lst)))]))
(check-expect (removedupes '(a a a a b b b)) '(a b))


;;##################################################################################;;
;;#44444444444444444444444444444444444444444444444444444444444444444444444444444444#;;
;;#44444444444444444444444444444444444444444444444444444444444444444444444444444444#;;
;;#44444444444444444444444444444444444444444444444444444444444444444444444444444444#;;
;;##################################################################################;;

;;KLAUSURBEISPIELAUFGABEN
;;1. Einfügen in eine Liste
;; insrt: num num (listof num) -> (listofnum)
(define (insrt number position list)
  (cond
    [(= 0 position) (cons number list)]
    [(empty? list) empty]
    [else (cons (first list) (insrt number (- position 1) (rest list)))]
    ))

;;2. Statistik einer Zahlenliste
;; foo1: list -> (listof min avg max)
(define (foo1 list1)
  (local(
         (define (foo2 list2 mini maxi avg)
           (cond
             [(empty? list2) (list mini avg maxi)]
             [else (foo2 (rest list2)
                         (min mini (first list2))
                         (max maxi (first list2))
                         (+ avg (/ (first list2)
                                   (length list1))))]
             )))
    (foo2 list1 (first list1) (first list1) 0)))

;;3. Aufbau eines Binärbaums
(define-struct node (value left right))

(define (foo2 nodes)
  (cond
    [(empty? nodes) empty]
    [else (local(
                 (define (insrt tree node)
                   (cond
                     [(empty? tree) node]
                     [(< (node-value tree) (node-value node)) (make-node (node-value tree) (node-left tree) (insrt (node-right tree) node))]
                     [else (make-node (node-value tree) (insrt (node-left tree) node) (node-right tree))]
                     )))
            (insrt (foo2 (rest nodes)) (first nodes)))]))



;; 6. STRING MANIPULATION
;; 6.1 String in umgekehrter Reihenfolge
(define (reverse-str str)
  (implode (reverse (explode str))))
(check-expect (reverse-str "audi") "idua")

;; 6.2  Konkatenation von Strings
(define (conc-str str1 str2)
  (cond
    [(equal? str1 str2) str1]
    [else (implode(append (explode str1) (explode str2)))]))
(check-expect (conc-str "audi" "audi") "audi")
(check-expect (conc-str "audi" "bmw") "audibmw")

;; 6.3
(define-struct str-pair (str1 str2))
(define (conc-pair-lst strlst)
  (cond
    [(empty? strlst) strlst]
    [else (cons (conc-str (str-pair-str1 (first strlst)) (str-pair-str2 (first strlst)))
                  (conc-pair-lst (rest strlst)))]
    ))
(define s1 (make-str-pair "audi" "bmw"))
(define s2 (make-str-pair "opel" "skoda"))
(define carlist (list s1 s2))
(check-expect (conc-pair-lst carlist) (list "audibmw" "opelskoda"))

;; 7. Sortieren einer Liste in aufsteigender Reihenfolge
(define-struct lst-element (value next))
(define l1 (make-lst-element 10 (make-lst-element 9 (make-lst-element 8 empty))))

(define (sort-lst givenstr)
  (local( (define (lstbuild struc)
            (cond
              [(null? struc) empty]
              [else (cons (lst-element-value struc) (lstbuild (lst-element-next struc)))]
              ))
          (define (lstbuilder lst)
            (cond
              [(empty? lst) empty]
              [else (make-lst-element (first lst) (lstbuilder (rest lst)))]))
        ) 
    (lstbuilder (sort (lstbuild givenstr) <)))
  )
(check-expect (sort-lst l1) (make-lst-element 8 (make-lst-element 9 (make-lst-element 10 '()))))

;; ADDITIONAL STUFF FOR FUN!
;; n is the length of the list!
(define (createlist n)
  (cond
    [(= 0 n) empty]
    [else (cons (random 10) (createlist (- n 1)))]))

(define (lstbuilder lst)
            (cond
              [(empty? lst) empty]
              [else (make-lst-element (first lst) (lstbuilder (rest lst)))]))

(define l2 (lstbuilder (createlist 20)))

;; 8. Durchsuchen einer List
(define (find-lst givenlst number)
  (local(
         (define (lstbuild struc) ;; build a normal list out of structure tree.
            (cond
              [(null? struc) empty]
              [else (cons (lst-element-value struc) (lstbuild (lst-element-next struc)))]))
         (define (quicker lst n start) ;; recursion of a list and a variable to track current position.
           (cond
             [(empty? lst) empty]
             [(= number (first lst)) (cons start (quicker (rest lst) n (+ start 1)))]
             [else (quicker (rest lst) n (+ start 1))  ]))
         )
    (quicker (lstbuild givenlst) number 0)))
(check-expect (find-lst l1 8) (list 2))
(check-expect (find-lst l1 10) (list 0))

;; 9. Matrizenaddition
(define matrix1 (list (list 11 12 13 14) (list 21 22 23 24) (list 31 32 33 34)))
(define matrix2 (list (list 11 12 13 13) (list 100 100 100 100) (list 31 69 69 22)))
(define (matrixadd ma1 ma2)
  (cond
    [(or (empty? ma1) (empty? ma2)) empty]
    [(equal? (map length ma1) (map length ma2))(cons (map + (first ma1) (first ma2)) (matrixadd (rest ma1) (rest ma2)))]
    [else empty]))

(check-expect (matrixadd matrix1 matrix2) (list (list 22 24 26 27) (list 121 122 123 124) (list 62 101 102 56)))
(check-expect (matrixadd matrix1 (list (list 11 1 1 1) (list 1 1 1 1))) empty)
;;##################################################################################;;
;;##################################################################################;;
;;##################################################################################;;
;;##################################################################################;;
;;##################################################################################;;

;; FROM IMPORTANT.RKT
(define 1l '(1 2 3 4))
(define 2l '(2 7 9))
(define t1 '(8 7 9 10 6))

(define (avg list)
  (cond
    [(empty? list) 0]
    [else (/
            (sum list)
            (length list))]))
(define (suma list)
  (cond
    [(empty? list) 0]
    [else (+ (first list) (sum (rest list)))]))


;; varianz
(define (deviation list)
  (cond
    [(empty? list) 0]
    [else (+ (sqr (- (first list) (avg list))
             (deviation (rest list))))]))
;; standardabweichung
(define (abv list)
  (sqrt (/ (deviationas list (avg list))
           (- (length list) 0))))
(define (deviationas list aver)
  (cond
    [(empty? list) 0]
    [else (+ (sqr (- (first list) aver))
             (deviationas (rest list) aver))]))












