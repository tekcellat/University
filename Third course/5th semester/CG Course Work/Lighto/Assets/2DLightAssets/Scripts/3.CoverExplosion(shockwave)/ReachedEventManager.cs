using UnityEngine;
using System.Collections;

public class ReachedEventManager : MonoBehaviour {

	DynamicLight light2d;
	GameObject myGO;
	GameObject[] GOsReached;



	// Use this for initialization
	void Start () {
		light2d = GameObject.Find("2DLight").GetComponent<DynamicLight>() as DynamicLight;
		myGO = GameObject.Find("hexagon");

		// Add listener
		light2d.OnReachedGameObjects += waveReach;



	}




	void waveReach(GameObject g){

		if(gameObject.GetInstanceID() == g.GetInstanceID()){
			Debug.Log(" _" + g.name +"__" + Time.time);
			//gameObject.GetComponent<SpriteRenderer>().sharedMaterial.color = Color.green;
		}else{
			//gameObject.GetComponent<SpriteRenderer>().sharedMaterial.color = Color.white;
		}

	}


}
