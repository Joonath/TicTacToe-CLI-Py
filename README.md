# CLI TicTacToe

Game TicTacToe dengan ukuran papan `nxn`.

### Program Flow
1. User inisiasi game dengan `TicTacToe()`
2. User diminta untuk menginput apakah game dilakukan secara multiplayer (`self.multiplayer = 1`) atau solo (`self.multiplayer = 2`) 
3. User diminta untuk menginput nama pemain 1 (`self.name["player1"]`) --> ulangi input ke-2 utk `player2` apabila permainan dilakukan secara multiplayer
3. Khusus utk single-player, User diminta untuk menginput tingkat kesulitan permainan dari skala 1 (paling mudah) hingga 5 (tidak mungkin menang) yg dimasukkan kedalam variabel `self.diffThreshold`
4. User diminta untuk menginput ukuran papan (`size`) dengan tipe data `integer` dengan rentang nilai dari `__min_board_size` hingga `__max_board_size`
5. Program melakukan konversi terhadap `size` menuju tipe data `tuple` (`self.size = (self.size, self.size)`)
6. Program membuat array (`self.board`) dengan `numpy.zeros(shape)` dimana `shape = size --> type 'tuple'`
7. Program melakukan `print` terhadap board via function `getUserBoard()`. Fungsi `getUserBoard()` akan:
    * membaca setiap value dari numpy.array yang berbentuk 2D
    * melakukan konversi terhadap value:
        - 0 = Tidak ada aksi (bisa ditempati oleh pemain dan NPC), dikonversi menjadi `[ ]`
        - 1 = Player Move, dikonversi menjadi string `[X]`
        - 2 = NPC/Player 2 Move, dikonversi menjadi string `[O]`
8. Program mengeksekusi method `userMove()`, user diminta untuk menginput `move` yang akan dijalankan user dengan bentuk `angka, angka`. Apabila ditemukan input yang tidak sesuai, maka berikan error dan user diminta untuk mengulangi input hingga diterima
9. Program melakukan validasi terhadap `move` dengan menjalankan method `isMoveValid(move)`. Apabila berhasil, program melanjutkan dengan eksekusi method `placeMove(move)` 
10. Program melakukan pengecekan terhadap keadaan `self.board` setelah pemain 1 dan pemain 2 atau NPC menempatkan `move`; apakah sudah ditemukan pemenang atau belum melalui `self.checkWinner()`:
    * Program mengeksekusi method `self.hasLinedUp()` untuk mengecek apakah ditemukan rangkaian nilai yang bukan nol (0) dan berderet secara horizontal, vertikal, dan diagonal. Method ini mengembalikan nilai `list(boolean, int)` dan di-_assign_ ke variabel `winnerState`
        * `winnerState[0]` mengindikasikan apakah sudah ditemukan pemenang (True/False)
        * `winnerState[1]` mengindikasikan pemenang dari game ini, dengan nilai 1 sebagai pemain atau 2 sebagai pemain kedua/NPC
    * Program juga menangani kasus _draw_ dimana `winnerState[0] == False` dan papan `self.board` sudah tidak lagi memiliki value 0 pada seluruh matrix yg disediakan 
11. Dalam hal program belum menemukan pemenang dan masih ada `move` yang valid, maka program melakukan kalkulasi terhadap nilai `self.diffThreshold`, dimana:
    * Program akan men-generate angka random dari 0.0 hingga 1.0 kedalam variabel `rdm`
    * Apabila `rdm >= self.diffThreshold` maka program mengeksekusi `self.smartMove()` yang memprioritaskan move untuk menghalangi player dalam memenangi permainan
    * Apabila `rdm < self.diffThreshold` maka program melakukan move secara acak menggunakan `self.computerMove()`
12. Program mengulangi tahapan 11, apabila belum ditemukan pemenang, maka kembali ke tahapan 8


### Config
`__min_board_size: int` <br>
Ukuran terkecil papan main. Disarankan 3.

`__max_board_size: int` <br>
Ukuran terbesar papan main. Disarankan 5.

### End Game Pattern:

```
=== 3x3 ===
     [X][X][X]        |      [X][ ][ ]       |     [X][ ][ ]
     [ ][ ][ ]        |      [X][ ][ ]       |     [ ][X][ ]
     [ ][ ][ ]        |      [X][ ][ ]       |     [ ][ ][X]
([0,0],[0,1],[0,2])   | ([0,0],[1,0],[2,0])  |([0,0],[1,1],[2,2])
([1,0],[1,1],[1,2])   | ([0,1],[1,1],[2,1])  |([0,2],[1,1],[2,0])
([2,0],[2,1],[2,2])   | ([0,2],[1,2],[2,2])  |

=== 4x4 ===
 [X][ ][ ][ ]
 [X][ ][ ][ ]
 [X][ ][ ][ ]
 [X][ ][ ][ ]
([0,0][0,1],[0,2],[0,3])
dst.

Pattern:
Bingo vertikal       | Bingo horizontal    | Bingo diagonal
numpy.array[::1, 0]  | numpy.array[0, ::1] | numpy.array[0,0] V numpy.array[0,2] ==> numpy.diagonal(array) or 
numpy.array[::1, 1]  | numpy.array[1, ::1] | numpy.array[1,1]                        numpy.diagonal(numpy.fliplr(array))
numpy.array[::1, 2]  | numpy.array[2, ::1] | numpy.array[2,2] V numpy.array[2,0]
dst                  | dst                 | dst
```
