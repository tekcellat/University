using UnityEngine;
using System.Collections;

public class interface_manager: MonoBehaviour {

	public GUIText UIlights;
	public GUIText UIvertex;

	GameObject cLight;
	GameObject cubeL;
	Camera cam;
	



	[HideInInspector] public static int vertexCount;

	int lightCount = 4;


	void Start () {

		cam = GameObject.Find("Camera").GetComponent<Camera>();

		Application.targetFrameRate = 60;

		cLight = GameObject.Find("2DLight");
	}
	
	// Update is called once per frame
	void Update () {

		//if(Input.GetAxis("Horizontal")){
		//light.transform.position = new Vector3 (Input.mousePosition.x -Screen.width*.5f, Input.mousePosition.y -Screen.height*.5f);
		Vector3 pos = cLight.transform.position;
		pos.x += Input.GetAxis ("Horizontal") * 30f * Time.deltaTime;
		pos.y += Input.GetAxis ("Vertical") * 30f * Time.deltaTime;
		cLight.transform.position = pos;


		if (Input.GetMouseButtonDown (0)) {

			Vector2 p = cam.ScreenToWorldPoint(Input.mousePosition);

			//if(Input.GetKey(KeyCode.LeftControl) == true){
				Material m = new Material( cLight.GetComponent<DynamicLight>().lightMaterial as Material); 
				

				GameObject nLight = new GameObject("2DLight" + (lightCount + 1));
				nLight.transform.parent = cLight.transform;
				
				nLight.AddComponent<DynamicLight>();
				//m.color = new Color(Random.Range(0f,1f),Random.Range(0f,1f),Random.Range(0f,1f));
				nLight.GetComponent<DynamicLight>().lightMaterial = m;
				nLight.transform.position = p;
				nLight.GetComponent<DynamicLight>().lightRadius = 40;
				
				GameObject quad = GameObject.CreatePrimitive(PrimitiveType.Quad);
				quad.transform.parent = nLight.transform;
				quad.transform.localPosition = Vector3.zero;
				lightCount++;
			
			//}



		}

		int totalV = cLight.GetComponent<DynamicLight>().vertexWorking;
		for (int i =1; i< lightCount; i++){
			totalV += cLight.transform.FindChild("2DLight" + (i+1)).gameObject.GetComponent<DynamicLight>().vertexWorking;
		}


		UIlights.text = "Lights: " + lightCount;
		UIvertex.text = "Working Vertexes: " + totalV;
	
	}



}
