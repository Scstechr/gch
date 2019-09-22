from src.util import validateRef as ref

ref('\x00')
ref('[')
ref('..')
