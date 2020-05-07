//--------------------------------------------------------------------------
// 
//  File: Scene.cs
//
//--------------------------------------------------------------------------
//
using System.Collections.Generic;

namespace MI
{
    class Scene
    {
        public SceneObject[] Things;
        public Light[] Lights;
        public Camera Camera;

        public Scene(SceneObject[] things, Light[] lights, Camera camera) { Things = things; Lights = lights; Camera = camera; }

        public IEnumerable<ISect> Intersect(Ray r)
        {
            foreach (SceneObject obj in Things)
            {
                yield return obj.Intersect(r);
            }
        }
    }
}
