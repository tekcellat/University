//--------------------------------------------------------------------------
// 
//  File: Ray.cs
//
//--------------------------------------------------------------------------
//
namespace MI
{
    struct Ray
    {
        public Vector Start;
        public Vector Dir;

        public Ray(Vector start, Vector dir) { Start = start; Dir = dir; }
    }
}
