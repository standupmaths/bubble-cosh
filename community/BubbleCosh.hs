{-- * Haskell implementation by MorrowM
    *
    * First download a copy of the GHC compiler:
    * https://www.haskell.org/downloads/
    * Then run:
      $ runghc community/BubbleCosh.hs
    *
    * Or, compile and run it with the following two commands:
      $ ghc community/BubbleCosh.hs -O -no-keep-hi-files -no-keep-o-files
      $ community/BubbleCosh
    * (on Windows run the generated .exe file instead)
    *
    * Note that the compiled version is orders of magnitude faster
    * than interpreting the file with runghc.
    *
    * Tested with GHC versions 8.10.7, 9.0.2, and 9.2.1
--}
import Data.Foldable (minimumBy)
import Data.Ord (comparing)
import Text.Printf (printf)

main :: IO ()
main = do
  let d = 1.068
      l = 0.6
      dl = DL d l
      ab@(AB a b) = abFinder dl
  printf "for diameters of %f and length of %f\n" d l
  print [a, b]

  let mid_radius = bubbleFunc ab (l / 2)
  printf "Area of %f\n" (totalArea dl ab)
  printf "mid dip of %f\n" (d / 2 - mid_radius)
  printf "mid gap of %f\n" (mid_radius * 2)

-- | A type for representing an error value.
newtype Error = Error Double
  deriving (Eq, Ord, Show)

-- | A data structure containing @a@ and @b@ values.
data AB = AB
  { aVal :: !Double
  , bVal :: !Double
  }
  deriving (Show)

-- | A data structure containing @d@ and @l@ values.
data DL = DL
  { dVal :: !Double
  , lVal :: !Double
  }
  deriving (Show)

-- | The cosh bubble function.
bubbleFunc :: AB -> Double -> Double
bubbleFunc (AB a b) x = a * cosh ((x - b) / a)

-- | Calculate the error for give values of @d@, @l@, @a@, and @b@.
calcError :: DL -> AB -> Error
calcError (DL d l) ab = Error $ errorAtX 0 + errorAtX l
 where
  y = d / 2
  errorAtX x = abs $ bubbleFunc ab x - y

-- | Find appropriate values of @a@ and @b@, given @d@ and @l@.
abFinder :: DL -> AB
abFinder dl = go (AB 1 1) (Error (1 / 0)) 0.1
 where
  -- The core loop. Take steps of a given step size, minimizing the error,
  -- then shrink the step size. Rinse and repeat until we've hit our target
  -- precision.
  go ab0 err0 step0
    | err0 < Error targetPrecision || step0 < targetPrecision = ab0
    | otherwise = go ab1 err1 (step0 / 10)
   where
    (ab1, err1) = performAllSteps err0 ab0 step0

  targetPrecision = 0.0000001

  -- Take a step in the direction that yields a minimal error value.
  performOneStep step0 (AB a0 b0) =
    minimumBy
      (comparing snd)
      [ (ab1, calcError dl ab1)
      | a1 <- [a0 - step0, a0, a0 + step0]
      , b1 <- [b0 - step0, b0, b0 + step0]
      , let ab1 = AB a1 b1
      ]

  -- Take as many steps of a given step size until we're no longer
  -- making any progress.
  performAllSteps err0 ab0 step =
    let (ab1, err1) = performOneStep step ab0
     in if err0 <= err1 then (ab0, err0) else performAllSteps err1 ab1 step

totalArea :: DL -> AB -> Double
totalArea (DL _d l) (AB a _b) = pi * a * a * (sinh (l / a) + l / a) -- Is this correct Matt? d and b are never used.
