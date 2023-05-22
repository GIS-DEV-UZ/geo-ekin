var map = null;
var geojsonFeatures = null;
var polygon = null
var userFeaturesList = [];

if (user_id != null) {
  fetch(`/get_polygons/${user_id}`)
    .then((res) => res.json())
    .then((res) => {
      res.polygon_cad_number.forEach((cadastral_number) => {
        fetch(
          `https://map.agro.uz/api/land_user/read_geom_all?prefix=${cadastral_number}`
        )
          .then((res) => res.json())
          .then((res) => {
            let property = res[0].features[0].properties;
            propObj = {
              cadastral_number: property.cadastral_number,
              legal_area: property.legal_area,
              tuman: property.tuman,
              arable_areas_with_water: property.arable_areas_with_water,
              baunit_type_title: property.baunit_type_title,
            };


            makeFeatureTable(propObj);
          });
      });
    });
}

$("#exampleModal").on("show.bs.modal", (event) => {
  if (!map) {
    map = L.map("map").setView([41.311081, 69.240562], 13);

    L.tileLayer("http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}", {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);
  }
  setTimeout(function () {
    window.dispatchEvent(new Event("resize"));
  }, 500);
});

$(".search_cadastr").click(function (e) {
  e.preventDefault();
  cadastral_number = $(".cad_number").val();
  fetch(
    `https://map.agro.uz/api/land_user/read_geom_all?prefix=${cadastral_number}`
  )
    .then((res) => res.json())
    .then((geojsonFeature) => {
      geojsonFeatures = geojsonFeature
      polygon = L.geoJSON(geojsonFeature).addTo(map);
      polygon.setStyle({ fillColor: "blue" });
      map.fitBounds(polygon.getBounds());
    });

    console.log(document.querySelector('.profile__msg').classList.contains('profile__msg-hide'))

    if(document.querySelector('.profile__msg').classList.contains('profile__msg-hide')){
      document.querySelector('.profile__msg').classList.remove('profile__msg-hide')
      document.querySelector('.profile__msg').classList.remove('profile__msg-show')
      document.querySelector('.profile__msg-content').classList.remove('alert-warning')
      document.querySelector('.profile__msg-content').classList.remove('alert-success')
    }
});

$(".save-polygon").click(function (e) {
  const properties = geojsonFeatures[0].features[0].properties;
  propObj2 = {
    cadastral_number: properties.cadastral_number,
    legal_area: properties.legal_area,
    arable_areas_with_water: properties.arable_areas_with_water,
    baunit_type_title: properties.baunit_type_title
  };

  let isPolygonHave = false
  
  userFeaturesList.forEach((feature, index) => {
    if(feature.cadastral_number == properties.cadastral_number) {
      document.querySelector('.profile__msg').classList.add('profile__msg-show')
      document.querySelector('.profile__msg-content').classList.add('alert-warning')
      document.querySelector('.profile__msg-content').textContent = "Bunday POLYGON allaqachon qo'shilgan"
      isPolygonHave = true
    }
  })

  if (!isPolygonHave){
    makeFeatureTable(propObj2);
    document.querySelector('.profile__msg').classList.add('profile__msg-show')
    document.querySelector('.profile__msg-content').classList.remove('alert-warning')
    document.querySelector('.profile__msg-content').classList.add('alert-success')
    document.querySelector('.profile__msg-content').textContent = ''
    document.querySelector('.profile__msg-content').textContent = "Polygon qo'shildi"
  }

  setTimeout(()=>{
    document.querySelector('.profile__msg').classList.add('profile__msg-hide')
  },5000)
  $(".cad_number").val('')

  map.removeLayer(polygon)

  fetch(`/save_polygon/${properties.cadastral_number}`)
    .then((res) => res.json())
    .then((res) => {
      console.log(res);
    });

});

function makeFeatureTable(featureObj) {
  userFeaturesList.push(featureObj);
  const elFarmerTableTbody = document.querySelector(
    ".profile-farmer__table tbody"
  );
  if (elFarmerTableTbody != null) {
    elFarmerTableTbody.innerHTML = "";
    userFeaturesList.forEach((feature, index) => {
      elFarmerTableTbody.innerHTML += `<tr>
          <td>${index+1}</td>
          <td>${feature.cadastral_number}</td>
          <td>${feature.legal_area}</td>
          <td>${feature.arable_areas_with_water}</td>
          <td>${feature.baunit_type_title} ga</td>
          <td>
            <a href="/user/polygon?cad_number=${feature.cadastral_number}">
              <img src="../static/images/eye.svg" alt="">
            </a>
          </td>
        </tr>`;
    });
  }
}