from GameClient import *

class OXOTextClient(GameClient):
    
    def __init__(self):
        GameClient.__init__(self)
        self.board = [' '] * BOARD_SIZE
        self.shape = None
        
    def clear_board(self):
        self.board = [' '] * BOARD_SIZE
        
    def input_server(self):
        return input('enter server:')
     
    def input_move(self):
        return input('enter move(0-8):')
     
    def input_play_again(self):
        return input('play again(y/n):')

    def display_board(self):
        # implement this method
        
        return """ 
              {} | {} | {}     0 | 1 | 2
              ---------
              {} | {} | {}     3 | 4 | 5
              ---------
              {} | {} | {}     6 | 7 | 8
              """.format(
                  self.board[0],self.board[1],self.board[2],
                  self.board[3],self.board[4],self.board[5],
                  self.board[6],self.board[7],self.board[8],
              )
              
    # Method that will write everything in the buffer to the terminal
    def outlit(self,msg):
        print("\n" + msg)
        sys.stdout.flush()
        
    def handle_message(self,msg):
        # implement this method
        
        # Check if server sent a message
        if msg:   
                    
            # Display board and character of player on a new game
            if msg == "new game,O" or msg == "new game,X":
                self.outlit(msg[:8] + ", your character is " + msg[9]) # display the character
                self.outlit(self.display_board())   # display board to players
                     
            # Check for current players move and print appropriate information
            if msg == 'your move':
                self.outlit("your move")  # write message in the buffer to terminal
                move = self.input_move() 
                self.send_message(move)  # send message to server
                
            elif msg == "opponents move":
                self.outlit("opponents move, wait for opponent to place a move...") # write message in the buffer to terminal
             
            # Check for message from the server (valid or invalid) 
            if str(msg[:10]) == "valid move":
                self.board[eval(msg[13])] = msg[11]  # insert symbol X or O in the board
                self.outlit(self.display_board())  # display board 
    
            elif str(msg[:12]) == "invalid move":
                self.outlit(msg)
                self.outlit("please enter a valid position on the board (0-8")
                self.outlit(self.display_board())  # display board     
                
            # check for message from the server (game over,(O,X,T) )
            if msg == "game over,O" or msg == "game over,X":
                self.outlit(msg[:9])
                self.outlit("Player " + msg[10] + " Wins!") # Display the winner
                
            elif msg == "game over,T":
                self.outlit(msg[:9])
                self.outlit("Its a Draw!") # write message in the buffer to terminal
            
            # Check for message from the sever (play again or exit game and reset board game)    
            if msg == "play again":
                
                # reset board for new game
                for position in range(9):
                    self.board[position] = ' '
                    
                answer = self.input_play_again()
                
                # Check for invalid inputs    
                while not ("y" == answer or answer == "n"):
                    self.outlit("Please enter y or n...") # write message in the buffer to terminal
                    answer = self.input_play_again()
                self.send_message(answer) # send message to server

            elif msg == "exit game":
                self.outlit("Someone ended the game") # write message in the buffer to terminal
                    
    def play_loop(self):
        while True:
            msg = self.receive_message()
            if len(msg): 
                self.handle_message(msg)
            else: 
                break
                
def main():
    otc = OXOTextClient()
    while True:
        try:
            otc.connect_to_server(otc.input_server())
            break
        except:
            print('Error connecting to server!')       
    otc.play_loop()
    input('Press click to exit.')
        
main()
