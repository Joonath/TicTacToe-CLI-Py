#!/usr/bin/env python
# coding: utf-8

# # CLI TicTacToe
# 
# Game TicTacToe dengan ukuran papan `nxn`.
# 
# ### Program Flow
# 1. User inisiasi game dengan `TicTacToe()`
# 2. User diminta untuk menginput apakah game dilakukan secara multiplayer (`self.multiplayer = 1`) atau solo (`self.multiplayer = 2`) 
# 3. User diminta untuk menginput nama pemain 1 (`self.name["player1"]`) --> ulangi input ke-2 utk `player2` apabila permainan dilakukan secara multiplayer
# 3. Khusus utk single-player, User diminta untuk menginput tingkat kesulitan permainan dari skala 1 (paling mudah) hingga 5 (tidak mungkin menang) yg dimasukkan kedalam variabel `self.diffThreshold`
# 4. User diminta untuk menginput ukuran papan (`size`) dengan tipe data `integer` dengan rentang nilai dari `__min_board_size` hingga `__max_board_size`
# 5. Program melakukan konversi terhadap `size` menuju tipe data `tuple` (`self.size = (self.size, self.size)`)
# 6. Program membuat array (`self.board`) dengan `numpy.zeros(shape)` dimana `shape = size --> type 'tuple'`
# 7. Program melakukan `print` terhadap board via function `getUserBoard()`. Fungsi `getUserBoard()` akan:
#     * membaca setiap value dari numpy.array yang berbentuk 2D
#     * melakukan konversi terhadap value:
#         - 0 = Tidak ada aksi (bisa ditempati oleh pemain dan NPC), dikonversi menjadi `[ ]`
#         - 1 = Player Move, dikonversi menjadi string `[X]`
#         - 2 = NPC/Player 2 Move, dikonversi menjadi string `[O]`
# 8. Program mengeksekusi method `userMove()`, user diminta untuk menginput `move` yang akan dijalankan user dengan bentuk `angka, angka`. Apabila ditemukan input yang tidak sesuai, maka berikan error dan user diminta untuk mengulangi input hingga diterima
# 9. Program melakukan validasi terhadap `move` dengan menjalankan method `isMoveValid(move)`. Apabila berhasil, program melanjutkan dengan eksekusi method `placeMove(move)` 
# 10. Program melakukan pengecekan terhadap keadaan `self.board` setelah pemain 1 dan pemain 2 atau NPC menempatkan `move`; apakah sudah ditemukan pemenang atau belum melalui `self.checkWinner()`:
#     * Program mengeksekusi method `self.hasLinedUp()` untuk mengecek apakah ditemukan rangkaian nilai yang bukan nol (0) dan berderet secara horizontal, vertikal, dan diagonal. Method ini mengembalikan nilai `list(boolean, int)` dan di-_assign_ ke variabel `winnerState`
#         * `winnerState[0]` mengindikasikan apakah sudah ditemukan pemenang (True/False)
#         * `winnerState[1]` mengindikasikan pemenang dari game ini, dengan nilai 1 sebagai pemain atau 2 sebagai pemain kedua/NPC
#     * Program juga menangani kasus _draw_ dimana `winnerState[0] == False` dan papan `self.board` sudah tidak lagi memiliki value 0 pada seluruh matrix yg disediakan 
# 11. Dalam hal program belum menemukan pemenang dan masih ada `move` yang valid, maka program melakukan kalkulasi terhadap nilai `self.diffThreshold`, dimana:
#     * Program akan men-generate angka random dari 0.0 hingga 1.0 kedalam variabel `rdm`
#     * Apabila `rdm >= self.diffThreshold` maka program mengeksekusi `self.smartMove()` yang memprioritaskan move untuk menghalangi player dalam memenangi permainan
#     * Apabila `rdm < self.diffThreshold` maka program melakukan move secara acak menggunakan `self.computerMove()`
# 12. Program mengulangi tahapan 11, apabila belum ditemukan pemenang, maka kembali ke tahapan 8
# 
# 
# ### Config
# `__min_board_size: int` <br>
# Ukuran terkecil papan main. Disarankan 3.
# 
# `__max_board_size: int` <br>
# Ukuran terbesar papan main. Disarankan 5.
# 
# ### End Game Pattern:

# ```
# === 3x3 ===
#      [X][X][X]        |      [X][ ][ ]       |     [X][ ][ ]
#      [ ][ ][ ]        |      [X][ ][ ]       |     [ ][X][ ]
#      [ ][ ][ ]        |      [X][ ][ ]       |     [ ][ ][X]
# ([0,0],[0,1],[0,2])   | ([0,0],[1,0],[2,0])  |([0,0],[1,1],[2,2])
# ([1,0],[1,1],[1,2])   | ([0,1],[1,1],[2,1])  |([0,2],[1,1],[2,0])
# ([2,0],[2,1],[2,2])   | ([0,2],[1,2],[2,2])  |
# 
# === 4x4 ===
#  [X][ ][ ][ ]
#  [X][ ][ ][ ]
#  [X][ ][ ][ ]
#  [X][ ][ ][ ]
# ([0,0][0,1],[0,2],[0,3])
# dst.
# 
# Pattern:
# Bingo vertikal       | Bingo horizontal    | Bingo diagonal
# numpy.array[::1, 0]  | numpy.array[0, ::1] | numpy.array[0,0] V numpy.array[0,2] ==> numpy.diagonal(array) or 
# numpy.array[::1, 1]  | numpy.array[1, ::1] | numpy.array[1,1]                        numpy.diagonal(numpy.fliplr(array))
# numpy.array[::1, 2]  | numpy.array[2, ::1] | numpy.array[2,2] V numpy.array[2,0]
# dst                  | dst                 | dst
# ```
# 

# # Script

# In[12]:


import numpy as n
import random as rand
from IPython.display import clear_output #utk refresh output di Jupyter

class TicTacToe():
    """
    # Ruleset:
    ### Move Indicator
    # 0 = No action
    # 1 = Player 1 Flag     --> X
    # 2 = NPC/Player 2 Flag --> O
    ###############
    ### End Game Criteria
    # - Berhasil menandai papan main secara vertikal, horizontal, ataupun diagonal
    # - Seri apabila tidak ada tanda yg lined up + langkah valid habis (mark '0' == 0) 
    """
    
    # Config
    # Instance-shared variables; Variabel utk semua instance Game() yg aktif. Ubah utk menyesuaikan
    __min_board_size = 3
    __max_board_size = 7
    
    def __init__(self):
        
        print(
        '''
        Selamat datang di game TicTacToe!
        ''')
        
        self.multiplayer = 2 # 1=True, 2=False
        self.name = {}
        
        while True:
            try:
                self.multiplayer = int(input(
                        """
            Apakah kamu akan bermain bersama dengan teman manusia?
            1. Ya, saya ada teman nih!
            2. Tidak, saya sendiri aja
            Input: [1..2]:"""
                    )
              )
            except ValueError:
                clear_output(wait = True)
                print("Ups, harap gunakan input angka 1 hingga 2. Coba lagi!")
                continue
            else:
                if self.multiplayer not in [1,2]: 
                    clear_output(wait=True)
                    continue
                break
        
        
        self.name["player1"] = input("Masukkan nama Player 1: ")
        
        if self.multiplayer == 1: #kalau mainnya berdua
            self.name["player2"] = input("Masukkan nama Player 2: ")
        else:
            while True:
                try:
                    self.difficulty = int(input("""
            Mau seberapa susah game nya?
            1. No-brainer
            2. Mudah
            3. Lumayan
            4. Susah
            5. Pasti Kalah (atau seri ;))
            Input [1..5]:"""))
                except ValueError:
                    clear_output(wait = True)
                    print("Ups, harap gunakan input angka 1 hingga 5. Coba lagi!")
                else:
                    if self.difficulty < 1 or self.difficulty > 5: 
                        clear_output(wait=True)
                        continue
                    break
        
        self.diffThreshold = {
            1: 1.0,
            2: 0.95,
            3: 0.88,
            4: 0.5,
            5: 0.0
        }
        
        self.diffThreshold = self.diffThreshold[self.difficulty]

#         print("Oke, thresholdnya adalah ", self.diffThreshold)
        
        while True: #Looping action input sampai hasilnya valid
            try:
                self.size = int(input(
                        "Masukkan size papan permainan yang kamu inginkan [{}..{}]: ".format(
                            self.__min_board_size, self.__max_board_size
                        )
                ))
            except ValueError: #Kalau inputan self.size selain integer
                clear_output(wait = True)
                print("Ups sepertinya terjadi kesalahan! Mohon hanya gunakan angka {} hingga {}. Coba lagi yuk!".format(
                    self.__min_board_size, self.__max_board_size
                ))
                continue
            else:
                if self.size >= self.__min_board_size and self.size <= self.__max_board_size: #kalau valid:
                    break #keluar dari while Loop
                else: #kalau ga valid:
                    clear_output(wait = False)
                    print("Ups, ukuran papan yang diperbolehkan hanya angka dari {} hingga {}. Coba lagi yuk!".format(
                        self.__min_board_size, self.__max_board_size
                    ))
                    continue
        
        self.size = (self.size, self.size)
        self.board = n.zeros(shape = self.size, dtype="int")
        
        
        #Game sudah diinisiasi di titik ini. Selanjutnya mainin input player & move si NPC/player 2
        
        #Toggle Comment utk debugging
        while True:
            
            self.userMove() #Input user
            
            # Cek apakah game udah memiliki pemenang
            if self.checkWinner(): break
            
            if self.multiplayer == 1:
                self.userMove(2)
            else:
                
                rdm = 0 + rand.random() * (1-0)
                
                if rdm >= self.diffThreshold:
                    self.smartMove()
                else:
                    self.computerMove() #Input random si NPC

            if self.checkWinner(): break
            # Kalo belom, lanjut self.userMove() / balik ke atas
        pass
    
    def checkWinner(self):
        winnerState = self.hasLinedUp() #Format list: [Boolean: Ada pemenang?, int: Siapa yang menang?]
        
        if winnerState[0] and winnerState[1] == 1: #kalo ketemu: initiate ending, break loop
            clear_output(wait = False)
            print("Selamat {}! Kamu telah memenangkan permainan ini!".format(self.name["player1"]))
            self.getUserBoard()
            return True
        
        elif not winnerState[0] and not n.any(self.board == 0):
            #kalo ga ada yg menang (False) dan udah ga ada move yg valid (mark "0" == 0) 
            clear_output(wait = False)
            print("Yah, game nya seri!")
            self.getUserBoard()
            return True
        
        elif winnerState[0] and winnerState[1] == 2: #kalo ketemu pemenang tapi bukan player 1 yg menang
            clear_output(wait = False)
            
            if self.multiplayer == 1: #Kalau multiplayer, ganti output
                print("Selamat {}! Kamu telah memenangkan permainan ini!".format(self.name["player2"]))
            else:
                print("Yah, kamu kalah dalam game ini...")
                
            self.getUserBoard()
            return True
        
        return False 
        pass
    
    def getUserBoard(self):
        """
        desc: Menampilkan papan main yg mudah dimengerti (simbol X, O dan kosong [ ]).
        """
    
        #Tambah satu row di ujung atas + satu column di ujung kiri --> numpy.pad( papan, (1,0) )
        b = n.pad(self.board, (1,0), mode="constant", constant_values = 9) 
        x,y = b.shape #Shape setelah ditambahin row & col

        for row in range(x):
            for col in range(y):
                if row == 0:
                    if col == 0: #row = 0 & col = 0 --> ujung kiri atas. Cukup kosongin
                        print(" \t", end = "")
                    else:
                        print(" ", col, "\t", end = "") #utk nomor/guide pemain dlm nentuin posisi col
                else:
                    if col == 0:
                        print(" " * 3, row, "\t", end = "") #utk nomor/guide pemain dlm nentuin posisi row
                    else:
                        print(
                            str(b[row, col]).replace("0", "[   ]").replace("1", "[ X ]").replace("2", "[ O ]"), 
                            "\t", 
                            end = ""
                        )

            print()
        pass
    
    def userMove(self, executor = 1):
        clear_output(wait = True)
        
        currently_playing = self.name["player1"] if executor == 1 else self.name["player2"]
        symbol = "X" if executor == 1 else "O"
        print("""
        Giliranmu, {}!
        
        Simbol kamu adalah "{}"
        Masukkan langkah dengan mengetikkan nomor urut baris dan kolom.
        Contoh: 3,2
        ======= 
        """.format(currently_playing, symbol))
        keepLoop = True
        
        while keepLoop:
            
            self.getUserBoard()
            move = input("Masukkan langkah [baris, kolom]: ") #3,2

            try:
                parsed_move = list(map(int, move.strip().split(",")))
            except TypeError:
                clear_output(wait = True)
                print("Ups, terjadi kesalahan! Mohon gunakan format yang benar (baris, kolom)!")
                continue
            except ValueError:
                clear_output(wait = True)
                print("Ups, terjadi kesalahan! Mohon untuk menggunakan angka saja!")
                continue
            else:
                #DEBUG: print("Input diterima! Value = %s" % parsed_move)
                
                if( len(parsed_move) != 2 ):
                    clear_output(wait = True)
                    print("Ups, terjadi kesalahan! Mohon untuk melakukan input dengan format (baris, kolom). Coba lagi!")
                    continue
                else:
                    if self.isMoveValid(parsed_move):
#debug                  print("masuk isMoveValid")
                        self.placeMove(parsed_move, executor)
                        
                        keepLoop = False
                    else:
                        clear_output(wait = True)
                        print("Posisi yang diinput tidak valid atau sudah ditempati. Coba lagi!")
                        continue

    def isMoveValid(self, parsed_move: list):
        """
        desc: Validasi apakah move player/NPC diperbolehkan. Kriteria:
              - Value di posisi (row,col) saat itu harus "0" (return True)
              - Selain 0, larang (return False)
              - (row, col) harus valid. Ga valid --> IndexError (return False)
        """
        row, col = [move_index - 1 for move_index in parsed_move]
        
        if row < 0 or col < 0:
            return False #gaboleh input 0 atau dibawahnya
        
        try:
            if self.board[row, col] == 0:
                return True
        except IndexError:
            clear_output(wait=True)
            print("Ups, terjadi kesalahan!",
              "Posisi yang kamu tentukan tidak benar.",
              "Mohon untuk menggunakan angka dari 1 hingga {}".format(self.size[0]))
            return False
        pass
    
    def placeMove(self, parsed_move: list, executor: int):
        row, col = [move_index - 1 for move_index in parsed_move]
        
        self.board[row, col] = executor
        pass
            
    def computerMove(self):
        while True:
            parsed_move = list(map(int, [rand.randint(0, self.size[0]), rand.randint(0, self.size[0])]))
            if self.isMoveValid(parsed_move):
                self.placeMove(parsed_move, 2)
                break
        pass
    
    def smartMove(self):
        #numpy.where return = tuple of numpy.array --> (np.array([...]), np.array([...]))
        #utk ambil value di dlm numpy.array --> np.where()[0] CASE row/col sudah ditetapkan/fixed
        
        #Debug, konfirmasi apakah random masuk ke validasi ini:
#         print("Masuk ke smartMove")
        
        x,y = self.size
        #Cek horizontal
        for row in range(x):
            if n.count_nonzero(self.board[row, ::1]) < x: #kalau dlm sederet masih ada 0 : 
                if len(n.where(self.board[row, ::1] == 1)[0]) == (x-1): #kalau dlm sederet itu sudah ada mark dari Player 1 sejumlah x-1:
                    
                    lastZero = n.where(self.board[row, ::1] == 0)[0][0] #ambil index kolom dengan value 0 yg terakhir di deret itu
                    
                    move = [row + 1, lastZero + 1] #Menyesuaikan dengan adjustment di placeMove dimana index - 1
#DEBUG                     print("\n\n===Masuk ke horizontal @ {}\n===".format(move))
                    
                    self.placeMove(move, 2)
                    return #selesai
                else: continue #selain itu lanjut ke row berikutnya
        
        #Cek vertikal
        for col in range(y):
            if n.count_nonzero(self.board[::1, col]) < y: #kalau dlm sederet masih ada 0 :
                if len(n.where(self.board[::1, col] == 1)[0]) == (y-1): #kalau dlm sederet itu sudah ada mark dari Player 1 sejumlah y-1:
                    lastZero = n.where(self.board[::1, col] == 0)[0][0] #ambil index row dengan value 0 terakhir di deret itu
                    move = [lastZero + 1, col + 1]
                    
#DEBUG                     print("\n\n===Masuk ke vertikal @ {}\n===".format(move))
                    
                    self.placeMove(move, 2)
                    return #selesai
                else: continue
                    
        #Cek diagonal
        if n.count_nonzero(n.diagonal(self.board)) < x: #kalau dlm diagonal ini masih ada 0 :
            if len(n.where(n.diagonal(self.board) == 1)[0]) == (x-1): #kalau dlm diagonal ini sudah ada mark dari PLayer 1 sebanyak x-1:
                lastZero = n.where(n.diagonal(self.board) == 0)[0][0] #ambil index row, col dengan value 0 terakhir (hint: row = col)
                move = [lastZero + 1, lastZero + 1]
                
#DEBUG                 print("\n\n===Masuk ke diagonal normal @ {}\n===".format(move))
                    
                
                self.placeMove(move, 2)
                return
        elif n.count_nonzero(n.diagonal(n.fliplr(self.board))) < x: 
            if len(n.where(n.diagonal(n.fliplr(self.board)) == 1)[0]) == (x-1):
                lastZero = n.where(n.diagonal(n.fliplr(self.board)) == 0)[0][0]
                
                #Special case: papannya dibalik dulu
                self.board = n.fliplr(self.board)
                
                move = [lastZero + 1, lastZero + 1]
                
#DEBUG                 print("\n\n===Masuk ke diagonal mirror @ {}\n===".format(move))
                
                self.placeMove(move, 2)
                
                #Dibalik lagi papannya
                self.board = n.fliplr(self.board)
                return
                
        #Case belum ketemu untuk di block:
#DEBUG         print("===\nNormal execution\n===")
        self.computerMove()
        pass
    
    def hasLinedUp(self) -> list:
        """
        desc: cek apakah sudah ada pemenang di sesi game ini.
        """
        x, y = self.size

        foundLinedUp = [False, False] #pakai list untuk simpan apakah ketemu pemenang @ index 0 + siapa yang menang @ index 1
        
        #vertikal
        for column in range(y):    
            if n.all(self.board[::1, column] == self.board[0, column]) and self.board[0, column] != 0:
                foundLinedUp = [True, self.board[0, column]]
                return foundLinedUp #langsung stop function; tdk perlu jalanin bawah
                
        #horizontal
        for row in range(x):
            if n.all(self.board[row, ::1] == self.board[row, 0]) and self.board[row, 0] != 0:
                foundLinedUp = [True, self.board[row, 0]]
                return foundLinedUp 
                
        #diagonal
        if n.all(n.diagonal(self.board) == self.board[0,0]):
            foundLinedUp = [True, self.board[0, 0]]
            
        elif n.all(n.diagonal(n.fliplr(self.board)) == self.board[0, y-1]): #x-1 dan y-1 utk penyesuaian ke zero-based index
            foundLinedUp = [True, self.board[0, y-1]]
            
        return foundLinedUp
        
        pass
        
    


# In[ ]:


game = TicTacToe()


# In[ ]:




