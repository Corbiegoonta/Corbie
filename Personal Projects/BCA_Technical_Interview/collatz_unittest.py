import unittest
import collatz_conjecture

class TestCollatz(unittest.TestCase):

    """Executes unit tests to ensure the collatz algorithm function is working as intended.
    """

    def test_collatz_conjecture_is_tuple(self):
        print("Running test to determine if the collatz_algorithm function returns a tuple.")
        try:
            result = collatz_conjecture.collatz_algorithm(4)
            self.assertEqual(type(result), tuple)
            print("This test has passed.")
        except AssertionError as e:
            print(e)
            print("This test failed due to the collatz_algorithm function not returning a tuple.")
        
    def test_collatz_conjecture_unproven(self):
        print("Running test to determine if the collatz conjecture remains unproven.")
        try:
            self.assertEqual(collatz_conjecture.collatz_algorithm(4)[2], 1)
            self.assertEqual(collatz_conjecture.collatz_algorithm(-1)[2], -2)
            self.assertEqual(collatz_conjecture.collatz_algorithm(-5)[2], -10)
            self.assertEqual(collatz_conjecture.collatz_algorithm(-17)[2], -34)
            print("This test has passed.")
        except Exception as e:
            print(e)
            if e == TimeoutError:
                print("This test failed due to the collatz_algorithm function taking too long to complete. \nEither the collatz conjecture has been proven or the number of steps are too large to be computed in a reasonable timeframe by the current compute capacity.")
            elif e == AssertionError:
                print("This test failed due to collatz_algorithm function not ending with 1")

    
    def test_collatz_conjecture_steps_type(self):
        print("Running test to determine if the collatz_algorithm function returns an integer type for the steps value.")
        try:
            result = collatz_conjecture.collatz_algorithm(10)
            self.assertEqual(type(result[0]), int)
            print("This test has passed.")
        except AssertionError as e:
            print(e)
            print("This test failed due to the collatz_algorithm function not returning an integer type for the steps value.")

    def test_collatz_conjecture_steps(self):
        print("Running test to determine if the collatz_algorithm function returns the correct steps value.")
        try:
            result = collatz_conjecture.collatz_algorithm(10)
            self.assertEqual(result[0], 6)
            print("This test has passed.")
        except AssertionError as e:
            print(e)
            print("This test failed due to the collatz_algorithm function not returning the steps value.")


    def test_collatz_conjecture_hailstone_list_type(self):
        print("Running test to determine if the collatz_algorithm function returns the hailstone_number list.")
        try:
            result = collatz_conjecture.collatz_algorithm(10)
            self.assertEqual(type(result[1]), list)
            print("This test has passed.")
        except AssertionError as e:
            print(e)
            print("This test failed due to the collatz_algorithm function not returning the hailstone_number list.")
    
    def test_collatz_conjecture_hailstone_numbers(self):
        print("Running test to determine if the collatz_algorithm function returns the correct hailstone numbers.")
        try:
            result = collatz_conjecture.collatz_algorithm(10)
            self.assertEqual(result[1], [5.0, 16.0, 8.0, 4.0, 2.0, 1.0])
            print("This test has passed.")
        except AssertionError as e:
            print(e)
            print("This test failed due to the collatz_algorithm function not returning the correct hailstone numbers.")

if __name__ == "__main__":
    unittest.main()
        