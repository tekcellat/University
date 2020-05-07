using UnityEngine;
using UnityEditor;
using System.Collections;

[CustomEditor (typeof (DynamicLight))] 
public class DynamicLightEditor : Editor {

	[MenuItem ("GameObject/Create Other/2D Dynamic Light/Add Light Point")]
	static void Create(){
		GameObject gameObject = new GameObject("2DLight");
		DynamicLight s = gameObject.AddComponent<DynamicLight>();
		s.Rebuild();
	}

	[MenuItem ("GameObject/Create Other/2D Dynamic Light/Add Gradient Light Point")]
	static void addGradient(){
		
		Material m = AssetDatabase.LoadAssetAtPath("Assets/2DLightAssets/Materials/StandardLightMaterialGradient.mat", typeof(Material)) as Material;
		GameObject gameObject = new GameObject("2DLight");
		DynamicLight s = gameObject.AddComponent<DynamicLight>();
		s.setMainMaterial(m);
		s.Rebuild();
		
	}


	[MenuItem ("GameObject/Create Other/2D Dynamic Light/Casters/Empty", false, 3)]
	static void addEmpty(){
		
		GameObject empty = new GameObject("empty");
		empty.layer = 8;
		empty.AddComponent<SpriteRenderer>();
		GameObject emptyChild = new GameObject("collider");
		emptyChild.AddComponent<PolygonCollider2D>();
		emptyChild.transform.parent = empty.transform;
		emptyChild.layer = 8;
		empty.transform.position = new Vector3(5,0,0);
		
	}

	[MenuItem ("GameObject/Create Other/2D Dynamic Light/Casters/Square")]
	static void addSquare(){
		
		Object prefab = AssetDatabase.LoadAssetAtPath("Assets/2DLightAssets/Prefabs/square.prefab", typeof(GameObject));
		GameObject hex = Instantiate(prefab, Vector3.zero, Quaternion.identity) as GameObject;
		hex.transform.position = new Vector3(5,0,0);
		hex.name = "square";
		
	}

	[MenuItem ("GameObject/Create Other/2D Dynamic Light/Casters/Hexagon")]
	static void addHexagon(){

		Object prefab = AssetDatabase.LoadAssetAtPath("Assets/2DLightAssets/Prefabs/hexagon.prefab", typeof(GameObject));
		GameObject hex = Instantiate(prefab, Vector3.zero, Quaternion.identity) as GameObject;
		hex.transform.position = new Vector3(5,0,0);
		hex.name = "hexagon";

	}
	[MenuItem ("GameObject/Create Other/2D Dynamic Light/Casters/Pacman")]
	static void addPacman(){
		
		Object prefab = AssetDatabase.LoadAssetAtPath("Assets/2DLightAssets/Prefabs/pacman.prefab", typeof(GameObject));
		GameObject hex = Instantiate(prefab, Vector3.zero, Quaternion.identity) as GameObject;
		hex.transform.position = new Vector3(5,0,0);
		hex.name = "pacman";
		
	}
	[MenuItem ("GameObject/Create Other/2D Dynamic Light/Casters/Star")]
	static void addStar(){
		
		Object prefab = AssetDatabase.LoadAssetAtPath("Assets/2DLightAssets/Prefabs/star.prefab", typeof(GameObject));
		GameObject hex = Instantiate(prefab, Vector3.zero, Quaternion.identity) as GameObject;
		hex.transform.position = new Vector3(5,0,0);
		hex.name = "star";
	}



	public override void OnInspectorGUI () {
		DynamicLight obj;
		obj = target as DynamicLight;
		if (obj == null)
		{
			return;
		}
		
		//serializedObject.Update();
		
		SerializedProperty
			version = serializedObject.FindProperty("version"),
			lmaterial = serializedObject.FindProperty ("lightMaterial"),
			radius = serializedObject.FindProperty ("lightRadius"),
			segments = serializedObject.FindProperty ("lightSegments"),
			layerm = serializedObject.FindProperty ("Layer");


		EditorGUILayout.IntSlider(segments, 1, 20);
		EditorGUILayout.PropertyField(radius);
		EditorGUILayout.PropertyField(lmaterial);
		EditorGUILayout.PropertyField(layerm);

		string v = version.stringValue;

		EditorGUILayout.HelpBox("2D Light Package PRO version: " + v, MessageType.None);

		int nSeg = segments.intValue;
		if (nSeg <= 3) {
				EditorGUILayout.HelpBox("Segments must be 3 o Higher", MessageType.Warning);
		}

		if (GUILayout.Button("Refresh")){
			obj.Rebuild();
		}

		if (serializedObject.ApplyModifiedProperties()||
		    (Event.current.type == EventType.ValidateCommand &&
		 Event.current.commandName == "UndoRedoPerformed")) {
			foreach (DynamicLight s in targets) {
				s.Rebuild();
			}
		}

	}

	void OnDrawGizmos() {
		DynamicLight obj;
		obj = target as DynamicLight;
		if (obj == null)
		{
			return;
		}
		Gizmos.DrawIcon(obj.gameObject.transform.position, "Light Gizmo.tiff", true);
	}


}
